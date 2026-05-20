from __future__ import annotations

import json
from pathlib import Path

DEFAULT_METADATA_PATH = Path("artifacts/model_metadata.json")


def write_model_metadata(metadata: dict, path: Path = DEFAULT_METADATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
