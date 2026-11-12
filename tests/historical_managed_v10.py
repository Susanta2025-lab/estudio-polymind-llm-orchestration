"""Executed v10 sources, verified against the unchanged inventory/2 fixture.

Only changed inventory members are copied; all other bytes must still match.
This test-only renderer cannot authorize execution under the current inventory.
"""

import json
import sys
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/digestion_contracts"


def sources():
    inventory = json.loads((FIXTURES / "managed_prompt10.json").read_text())
    result = {}
    for name, expected in inventory["sources"].items():
        frozen = FIXTURES / "v10_sources" / (name + ".txt")
        raw = (frozen if frozen.exists() else ROOT / name).read_bytes()
        assert sha256(raw).hexdigest() == expected, name
        result[name] = raw
    return result


def generation_digest():
    hashes = {name: sha256(raw).hexdigest() for name, raw in sources().items()}
    return sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@contextmanager
def activate(patch, directory):
    """Replay unchanged v10 rendering, including its six-file config binding."""
    from documents.digestion import managed

    for name, raw in sources().items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    path = directory / "documents/digestion/managed.py"
    module = ModuleType("tests._frozen_managed_prompt10")
    module.__file__ = str(path)
    patch.setitem(sys.modules, module.__name__, module)
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)  # noqa: S102 - Hash-pinned test fixture.
    for name in ("StageProfile", "ManagedSettings", "ManagedSynthesisInference"):
        patch.setattr(managed, name, getattr(module, name))
    yield
