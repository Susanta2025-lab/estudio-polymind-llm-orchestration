"""Private operator-supervised verification. No HTTP routes or identity issuer."""

from documents.pilot.models import (
    PilotError,
    PilotPolicy,
    SessionApproval,
    SourceApproval,
)

__all__ = [
    "PilotError",
    "PilotPolicy",
    "SessionApproval",
    "SourceApproval",
    "SupervisedPilot",
]


def __getattr__(name):
    if name == "SupervisedPilot":
        from documents.pilot.service import SupervisedPilot

        return SupervisedPilot
    raise AttributeError(name)
