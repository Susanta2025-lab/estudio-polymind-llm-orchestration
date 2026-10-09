"""Explicit per-request principal binding for both existing memory adapters."""
from security.models import session_key


class ScopedMemory:
    def __init__(self, store, authority, principal):
        self.store, self.authority = store, authority
        self.snapshot = authority.snapshot(principal)
        self.provider = store.provider

    def get_history(self, session_id, limit=None):
        with self.authority.release(self.snapshot):
            history = self.store.get_history(session_key(self.snapshot.principal, session_id), limit)
            return [{k: v for k, v in m.items() if k != 'session_id'} for m in history]

    def append_exchange(self, session_id, query, answer):
        with self.authority.release(self.snapshot):
            self.store.append_exchange(session_key(self.snapshot.principal, session_id), query, answer)

    def clear_session(self, session_id):
        with self.authority.release(self.snapshot):
            self.store.clear_session(session_key(self.snapshot.principal, session_id))

    def check_readiness(self):
        return self.store.check_readiness()

    def close(self):
        pass  # Request facade does not own the shared backend.
