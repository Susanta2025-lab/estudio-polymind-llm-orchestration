"""Atomic hierarchical reservations. Unknown expense survives restart and periods."""
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import json
import time
from uuid import UUID, uuid4

from pydantic import Field, field_validator, model_validator

from documents.models import FrozenModel
from security.database import Database
from security.models import Action, SecurityError


class GovernanceError(RuntimeError):
    def __init__(self, category='governance_denied'):
        self.category = category if category in {'governance_denied', 'pricing_unavailable', 'reservation_conflict'} else 'governance_denied'
        super().__init__(self.category)


def money(value):
    if isinstance(value, (float, bool)):
        raise ValueError('Decimal strings required')
    d = Decimal(value)
    if not d.is_finite() or d < 0 or d > Decimal('1000000000000') or d.as_tuple().exponent < -12:
        raise ValueError('Invalid decimal amount')
    return d


class Price(FrozenModel):
    provider: str = Field(pattern=r'^[A-Za-z0-9_./:-]{1,128}$')
    model: str = Field(pattern=r'^[A-Za-z0-9_./:-]{1,256}$')
    input_price: Decimal
    output_price: Decimal
    price_unit: int = Field(gt=0, le=1000000000)

    _price = field_validator('input_price', 'output_price', mode='before')(money)

    @field_validator('price_unit')
    @classmethod
    def decimal_unit(cls, value):
        if value not in {10**i for i in range(10)}:
            raise ValueError('Price unit must be a decimal power of ten')
        return value

    def cost(self, input_tokens, output_tokens):
        with localcontext() as ctx:
            ctx.prec = 60
            return (self.input_price * input_tokens + self.output_price * output_tokens) / self.price_unit


class PricingCatalog(FrozenModel):
    version: str = Field(pattern=r'^[A-Za-z0-9_./:-]{1,128}$')
    currency: str = Field(pattern=r'^[A-Z]{3}$')
    effective_date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    operator_approved: bool
    prices: tuple[Price, ...] = Field(min_length=1, max_length=128)

    @model_validator(mode='after')
    def approved(self):
        if not self.operator_approved or len({(p.provider,p.model) for p in self.prices}) != len(self.prices):
            raise ValueError('Explicit approved unique catalog required')
        datetime.strptime(self.effective_date, '%Y-%m-%d')
        return self

    def price(self, provider, model):
        for price in self.prices:
            if (price.provider, price.model) == (provider, model):
                return price
        raise GovernanceError('pricing_unavailable')


class Limits(FrozenModel):
    requests_per_window: int = Field(gt=0)
    window_seconds: int = Field(gt=0, le=86400)
    interactive_concurrent: int = Field(gt=0)
    background_concurrent: int = Field(gt=0)
    reserved_tokens: int = Field(gt=0)
    daily_tokens: int = Field(gt=0)
    monthly_tokens: int = Field(gt=0)
    monthly_cost: Decimal

    _cost = field_validator('monthly_cost', mode='before')(money)


class QuotaPolicy(FrozenModel):
    version: str = Field(pattern=r'^[A-Za-z0-9_./:-]{1,128}$')
    owner: Limits
    tenant: Limits


SCHEMA = (
    'CREATE TABLE configuration (singleton INTEGER PRIMARY KEY, policy TEXT NOT NULL, catalog TEXT NOT NULL)',
    'CREATE TABLE reservations (ticket TEXT PRIMARY KEY, tenant TEXT NOT NULL, owner TEXT NOT NULL, identity TEXT NOT NULL, identity_key TEXT NOT NULL, workload TEXT NOT NULL, policy TEXT NOT NULL, catalog TEXT NOT NULL, provider TEXT NOT NULL, model TEXT NOT NULL, input INTEGER NOT NULL, output INTEGER NOT NULL, cost TEXT NOT NULL, actual_input INTEGER, actual_output INTEGER, actual_cost TEXT, state TEXT NOT NULL, created REAL NOT NULL, UNIQUE(tenant,owner,identity_key))',
    'CREATE TABLE events (event_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, owner TEXT NOT NULL, action TEXT NOT NULL, at REAL NOT NULL)',
)


class GovernanceLedger(Database):
    def __init__(self, path, policy, catalog, *, clock=time.time, event_limit=100000):
        if type(event_limit) is not int or not 1 <= event_limit <= 10000000:
            raise SecurityError('security_configuration')
        self.policy = QuotaPolicy.model_validate(policy.model_dump())
        self.catalog = PricingCatalog.model_validate(catalog.model_dump())
        self.clock, self.event_limit = clock, event_limit
        super().__init__(path, SCHEMA)
        with self.transaction() as db:
            row = db.execute('SELECT * FROM configuration WHERE singleton=1').fetchone()
            values = (self.policy.model_dump_json(), self.catalog.model_dump_json())
            if row and (row['policy'],row['catalog']) != values:
                raise SecurityError('security_configuration')
            db.execute('INSERT OR IGNORE INTO configuration VALUES(1,?,?)', values)

    def ready(self):
        if not super().ready():
            return False
        try:
            with self.transaction() as db:
                return db.execute('SELECT COUNT(*) FROM events').fetchone()[0] < self.event_limit
        except SecurityError:
            return False

    def _event(self, db, scope, action):
        if db.execute('SELECT COUNT(*) FROM events').fetchone()[0] >= self.event_limit:
            raise SecurityError('security_unavailable')
        db.execute('INSERT INTO events VALUES(?,?,?,?,?)',
                   (str(uuid4()),str(scope.tenant),str(scope.owner),action,self.clock()))

    def reserve(self, principal, identity, input_tokens, output_tokens, workload='INTERACTIVE'):
        from security.models import Principal
        if (type(principal) is not Principal or principal.expires <= self.clock()
                or identity.scope != principal.scope.identity() or type(identity.attempt) is not int or identity.attempt < 1
                or workload not in {'INTERACTIVE', 'DOCUMENT_BACKGROUND'}
                or type(input_tokens) is not int or type(output_tokens) is not int
                or input_tokens < 0 or output_tokens <= 0 or input_tokens + output_tokens > 1000000000):
            raise GovernanceError()
        price = self.catalog.price(identity.provider, identity.model)
        if self.catalog.effective_date > datetime.fromtimestamp(self.clock(), timezone.utc).strftime('%Y-%m-%d'):
            raise GovernanceError('pricing_unavailable')
        encoded = json.dumps(asdict(identity), default=str, sort_keys=True, separators=(',', ':'))
        identity_key = json.dumps([str(identity.job),str(identity.step),identity.attempt],separators=(',', ':'))
        # Only opaque identifiers and bounded operator configuration belong here.
        if len(encoded) > 2048 or type(identity.job) is not UUID or type(identity.step) is not UUID:
            raise GovernanceError()
        scope = principal.scope
        cost = price.cost(input_tokens, output_tokens)
        denied = False
        with self.transaction() as db:
            existing = db.execute('SELECT * FROM reservations WHERE tenant=? AND owner=? AND identity_key=?',
                (str(scope.tenant),str(scope.owner),identity_key)).fetchone()
            if existing:
                if (existing['input'],existing['output'],existing['workload'],existing['identity']) != (input_tokens,output_tokens,workload,encoded):
                    raise GovernanceError('reservation_conflict')
                return existing['ticket']
            now = self.clock()
            date = datetime.fromtimestamp(now, timezone.utc)
            day = date.replace(hour=0,minute=0,second=0,microsecond=0).timestamp()
            month = date.replace(day=1,hour=0,minute=0,second=0,microsecond=0).timestamp()
            rows = list(db.execute('SELECT * FROM reservations WHERE tenant=?', (str(scope.tenant),)))
            for limits, rs in ((self.policy.tenant,rows), (self.policy.owner,[r for r in rows if r['owner']==str(scope.owner)])):
                recent = [r for r in rs if r['created'] > now-limits.window_seconds]
                spent = [r for r in rs if r['state'] != 'RELEASED']
                unsettled = lambda r: r['state'] not in {'SETTLED','RELEASED'}
                tokens = lambda r: r['input']+r['output'] if unsettled(r) else r['actual_input']+r['actual_output']
                active = [r for r in spent if r['state'] in {'RESERVED','ADMITTING','STARTED'}]
                current = [r for r in active if r['workload']==workload]
                cap = limits.interactive_concurrent if workload=='INTERACTIVE' else limits.background_concurrent
                with localcontext() as ctx:
                    ctx.prec = 60
                    expense = sum((Decimal(r['cost'] if unsettled(r) else r['actual_cost'])
                                   for r in spent if r['created']>=month or unsettled(r)), Decimal(0))
                    denied |= (len(recent)>=limits.requests_per_window or len(current)>=cap
                        or sum(r['input']+r['output'] for r in spent if unsettled(r))+input_tokens+output_tokens > limits.reserved_tokens
                        or sum(tokens(r) for r in spent if r['created']>=day or unsettled(r))+input_tokens+output_tokens > limits.daily_tokens
                        or sum(tokens(r) for r in spent if r['created']>=month or unsettled(r))+input_tokens+output_tokens > limits.monthly_tokens
                        or expense+cost > limits.monthly_cost)
            if denied:
                self._event(db,scope,'ADMISSION_DENIED')
            else:
                ticket = str(uuid4())
                db.execute('INSERT INTO reservations VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,NULL,NULL,NULL,?,?)',
                    (ticket,str(scope.tenant),str(scope.owner),encoded,identity_key,workload,self.policy.version,
                     self.catalog.version,identity.provider,identity.model,input_tokens,output_tokens,str(cost),'RESERVED',now))
                self._event(db,scope,'RESERVED')
        if denied:
            raise GovernanceError()
        return ticket

    def transition(self, ticket, before, after):
        if (before,after) not in {('RESERVED','ADMITTING'),('ADMITTING','STARTED'),('ADMITTING','RELEASED')}:
            raise GovernanceError('reservation_conflict')
        with self.transaction() as db:
            changed = db.execute('UPDATE reservations SET state=? WHERE ticket=? AND state=?', (after,ticket,before)).rowcount
            if changed != 1:
                raise GovernanceError('reservation_conflict')

    def settle(self, ticket, usage):
        counts = (getattr(usage,'prompt_tokens',None),getattr(usage,'completion_tokens',None))
        if any(v is not None and (type(v) is not int or v < 0 or v > 1000000000) for v in counts):
            raise GovernanceError('reservation_conflict')
        known = all(v is not None for v in counts)
        with self.transaction() as db:
            row = db.execute('SELECT * FROM reservations WHERE ticket=?', (ticket,)).fetchone()
            if not row or row['state'] not in {'STARTED','UNKNOWN','SETTLED'}:
                raise GovernanceError('reservation_conflict')
            if row['state'] == 'SETTLED':
                if counts != (row['actual_input'],row['actual_output']):
                    raise GovernanceError('reservation_conflict')
                return
            if row['state'] == 'UNKNOWN' and any(old is not None and old != new
                    for old,new in zip((row['actual_input'],row['actual_output']),counts)):
                raise GovernanceError('reservation_conflict')
            cost = self.catalog.price(row['provider'],row['model']).cost(*counts) if known else None
            db.execute('UPDATE reservations SET actual_input=?,actual_output=?,actual_cost=?,state=? WHERE ticket=?',
                       (*counts,str(cost) if cost is not None else None,'SETTLED' if known else 'UNKNOWN',ticket))

    def usage(self, principal, authority, *, limit=100, offset=0):
        authority.authorize(principal,Action.USAGE_READ,principal.scope)
        if type(limit) is not int or not 1 <= limit <= 100 or type(offset) is not int or not 0 <= offset <= 10000:
            raise GovernanceError()
        with self.transaction() as db:
            return [dict(r) for r in db.execute('SELECT * FROM reservations WHERE tenant=? AND owner=? ORDER BY created,ticket LIMIT ? OFFSET ?',
                    (str(principal.scope.tenant),str(principal.scope.owner),limit,offset))]

    def tenant_usage(self, principal, authority):
        authority.authorize(principal,Action.TENANT_ADMIN)
        with self.transaction() as db:
            rows=list(db.execute('SELECT cost,actual_cost,state FROM reservations WHERE tenant=?',
                                 (str(principal.scope.tenant),)))
            with localcontext() as ctx:
                ctx.prec=60
                reserved=sum((Decimal(r['cost']) for r in rows if r['state'] not in {'SETTLED','RELEASED'}),Decimal(0))
                measured=sum((Decimal(r['actual_cost']) for r in rows if r['state']=='SETTLED'),Decimal(0))
            return {'currency':self.catalog.currency,'calls':len(rows),'unsettled_cost':str(reserved),'measured_cost':str(measured)}
