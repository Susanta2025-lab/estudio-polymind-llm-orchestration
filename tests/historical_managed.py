"""Hash-pinned v9 renderer for permanent historical contract characterizations.

These fixtures exercise current canonical validators, storage and worker against
preserved historical generation. They cannot authorize current v10 execution.
"""

import json
import sys
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent / "fixtures/digestion_contracts"
SOURCE = (ROOT / "managed_prompt9.py.txt").read_bytes()
assert (
    sha256(SOURCE).hexdigest()
    == json.loads((ROOT / "managed_prompt9.json").read_text())["managed_source_sha256"]
)
_module = ModuleType("tests._frozen_managed_prompt9")
sys.modules[_module.__name__] = _module
exec(compile(SOURCE, str(ROOT / "managed_prompt9.py.txt"), "exec"), _module.__dict__)  # noqa: S102 - Hash-pinned historical fixture only.
ExecutionContext = _module.ExecutionContext
ManagedSettings = _module.ManagedSettings
ManagedSynthesisInference = _module.ManagedSynthesisInference
StageProfile = _module.StageProfile
generation_schema = _module.generation_schema
classify_managed = _module.classify_managed
# Keep the active class identity so observation hooks still see production flow.
from documents.digestion.managed import ManagedDigestionHandler


@contextmanager
def activate(patch):
    from documents.digestion import managed

    for name in ("StageProfile", "ManagedSettings", "ManagedSynthesisInference"):
        patch.setattr(managed, name, globals()[name])
    patch.setattr(
        ManagedDigestionHandler, "analyze", _module.ManagedDigestionHandler.analyze
    )
    single = sys.modules.get("tests.performance.foundry_single_call")
    if single is not None:
        for name in ("StageProfile", "ManagedSettings", "ManagedSynthesisInference"):
            patch.setattr(single, name, globals()[name])
    yield


def generation_digest(version=9):
    """Recompute inventory/1 from preserved bytes, never the active inventory/2."""
    inventory = json.loads((ROOT / "managed_prompt9_inventory.json").read_text())
    hashes = {}
    for name, digest in inventory["sources"].items():
        source = (ROOT / "v9_sources" / (name + ".txt")).read_bytes()
        assert sha256(source).hexdigest() == digest
        hashes[name] = digest
    hashes["documents/digestion/managed.py"] = sha256(
        (ROOT / f"managed_prompt{version}.py.txt").read_bytes()
    ).hexdigest()
    return sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
