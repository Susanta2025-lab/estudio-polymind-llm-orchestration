"""Test-only adapter for the application's implicit dotenv constructor input.

Importing config.settings here would construct its singleton too early. Intercept
the public BaseSettings constructor instead, selecting only the application model
and its subclasses. No settings source or Pydantic private API is replaced.
"""

from functools import wraps
from inspect import signature

from pydantic_settings import BaseSettings


def isolate_application_settings(monkeypatch):
    """Suppress omitted dotenv input until the owning MonkeyPatch is undone."""
    original = BaseSettings.__init__
    constructor = signature(original)

    @wraps(original)
    def initialize(self, *args, **kwargs):
        application_model = any(
            cls.__module__ == "config.settings" and cls.__name__ == "Settings"
            for cls in type(self).__mro__
        )
        if application_model:
            supplied = constructor.bind_partial(self, *args, **kwargs)
            if "_env_file" not in supplied.arguments:
                kwargs["_env_file"] = None
        original(self, *args, **kwargs)

    monkeypatch.setattr(BaseSettings, "__init__", initialize)
