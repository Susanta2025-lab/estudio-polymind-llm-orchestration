"""L0 single-host run guard, composed with Phase 17E/17G, never a transport.

All stages/retries must share this private database. Full reservations are never
refunded during the run. Unknown work permanently blocks automatic continuation.
"""
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import time
from uuid import uuid4

from pydantic import Field, field_validator, model_validator

from documents.models import FrozenModel
from governance.ledger import GovernanceError, PricingCatalog, money
from security.database import Database


class Contract(FrozenModel):
    catalog: PricingCatalog
    provider: str
    model: str
    region: str = Field(min_length=1)
    tier: str = Field(min_length=1)
    price_source: str = Field(min_length=1)
    approved: bool
    currency: str
    maximum: Decimal
    # Explicit aggregate upper bounds for the approved run, not hourly rates.
    fixed_cost: Decimal
    extra_cost: Decimal
    attempts: int = Field(default=50, strict=True, ge=1, le=50)
    input_tokens: int = Field(default=25000, strict=True, ge=1, le=25000)
    output_tokens: int = Field(default=3000, strict=True, ge=1, le=3000)
    total_input: int = Field(default=1250000, strict=True, ge=1, le=1250000)
    total_output: int = Field(default=150000, strict=True, ge=1, le=150000)
    rpm: int = Field(default=2, strict=True, ge=1, le=2)
    tpm: int = Field(default=30000, strict=True, ge=1, le=30000)
    context: int = Field(strict=True, gt=0)

    @field_validator('maximum', 'fixed_cost', 'extra_cost', mode='before')
    @classmethod
    def validate_money(cls, value):
        try:
            return money(value)
        except (TypeError, InvalidOperation):
            raise ValueError('Explicit decimal amount required') from None

    @model_validator(mode='after')
    def valid(self):
        if (not self.approved or self.currency != self.catalog.currency
                or self.currency != 'EUR' or not 0 < self.maximum <= Decimal('5')
                or date.fromisoformat(self.catalog.effective_date) > date.today()
                or self.fixed_cost + self.extra_cost > self.maximum
                or self.input_tokens + self.output_tokens > min(self.context, self.tpm)):
            raise ValueError('Unapproved or incompatible financial contract')
        self.catalog.price(self.provider, self.model)
        return self

    def cost(self, calls):
        return (self.catalog.price(self.provider, self.model).cost(
            calls * self.input_tokens, calls * self.output_tokens)
            + self.fixed_cost + self.extra_cost)

    def fits(self, calls):
        return (type(calls) is int and 0 <= calls <= self.attempts
                and calls*self.input_tokens <= self.total_input
                and calls*self.output_tokens <= self.total_output
                and self.cost(calls) <= self.maximum)


SCHEMA = (
    'CREATE TABLE configuration (singleton INTEGER PRIMARY KEY, contract TEXT NOT NULL, stopped TEXT)',
    'CREATE TABLE calls (ticket TEXT PRIMARY KEY, started REAL NOT NULL, input INTEGER NOT NULL, output INTEGER NOT NULL, finished REAL, outcome TEXT, usage TEXT)',
)


class RunGuard(Database):
    """InferenceAdmissionPort wrapper; one outstanding call across every stage.

    A durable run reservation precedes downstream admission. A crash or denial
    leaves it outstanding and requires investigation; it never grants a retry.
    """
    def __init__(self, path, contract, admission, *, clock=time.time):
        self.contract = Contract.model_validate(contract.model_dump())
        self.admission, self.clock = admission, clock
        super().__init__(path, SCHEMA)
        with self.transaction() as db:
            encoded = self.contract.model_dump_json()
            old = db.execute('SELECT contract FROM configuration').fetchone()
            if old and old['contract'] != encoded:
                raise GovernanceError('reservation_conflict')
            db.execute('INSERT OR IGNORE INTO configuration VALUES(1,?,NULL)', (encoded,))

    def stop(self, reason):
        # Store a closed taxonomy only, never exceptions, prompts or endpoints.
        allowed = {'cancelled', 'admission', 'identity', 'usage', 'provider', 'evidence',
                   'publication', 'quality', 'dependency', 'budget', 'capability'}
        reason = reason if reason in allowed else 'provider'
        with self.transaction() as db:
            db.execute('UPDATE configuration SET stopped=COALESCE(stopped,?)', (reason,))

    def acquire(self, identity, estimated_input, reserved_output, workload='DOCUMENT_BACKGROUND'):
        c = self.contract
        reason = None
        token = str(uuid4())
        with self.transaction() as db:
            rows = list(db.execute('SELECT * FROM calls'))
            stopped = db.execute('SELECT stopped FROM configuration').fetchone()['stopped']
            recent = [r for r in rows if r['started'] > self.clock()-60]
            if stopped or any(r['finished'] is None for r in rows):
                reason = 'usage'
            elif (identity.provider, identity.model) != (c.provider, c.model):
                reason = 'identity'
            elif (type(estimated_input) is not int or type(reserved_output) is not int
                  or not 0 <= estimated_input <= c.input_tokens
                  or not 0 < reserved_output <= c.output_tokens):
                reason = 'capability'
            elif (not c.fits(len(rows)+1) or len(recent) >= c.rpm
                  or (len(recent)+1)*(c.input_tokens+c.output_tokens) > c.tpm):
                reason = 'budget'
            if reason:
                db.execute('UPDATE configuration SET stopped=COALESCE(stopped,?)', (reason,))
            else:
                db.execute('INSERT INTO calls VALUES(?,?,?,?,NULL,NULL,NULL)',
                           (token, self.clock(), c.input_tokens, c.output_tokens))
        if reason:
            raise GovernanceError()
        try:
            downstream = self.admission.acquire(identity, estimated_input, reserved_output, workload)
        except BaseException:
            self.stop('admission')
            raise
        return json.dumps([token, downstream])

    def finish(self, ticket, *, usage, outcome):
        token, downstream = json.loads(ticket)
        counts = (getattr(usage, 'prompt_tokens', None), getattr(usage, 'completion_tokens', None))
        total = getattr(usage, 'total_tokens', None)
        known = (all(type(x) is int and x >= 0 for x in counts)
                 and (total is None or type(total) is int and total == sum(counts)))
        within = known and counts[0] <= self.contract.input_tokens and counts[1] <= self.contract.output_tokens
        try:
            self.admission.finish(downstream, usage=usage, outcome=outcome)
        except BaseException:
            self.stop('admission')
            raise
        with self.transaction() as db:
            row = db.execute('SELECT * FROM calls WHERE ticket=?', (token,)).fetchone()
            if not row or row['finished'] is not None:
                raise GovernanceError('reservation_conflict')
            db.execute('UPDATE calls SET finished=?,outcome=?,usage=? WHERE ticket=?',
                       (self.clock() if within else None, 'success' if outcome == 'success' else 'failed',
                        json.dumps(dict(input=counts[0], output=counts[1], total=total)), token))
            if not within or outcome != 'success':
                db.execute('UPDATE configuration SET stopped=COALESCE(stopped,?)',
                           ('usage' if not within else 'provider',))
        # A settled provider failure is terminal above, but is not an admission denial.
        # Unknown/excess usage still raises and leaves the reservation unresolved.
        if not within:
            raise GovernanceError()

    def records(self):
        with self.transaction() as db:
            return [dict(r) for r in db.execute('SELECT * FROM calls ORDER BY started,rowid')]
