from __future__ import annotations
from pathlib import Path
import yaml

def load_metrics_spec(path: str | None) -> dict:
    if not path:
        return {}
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return (data or {}).get("metrics", {})