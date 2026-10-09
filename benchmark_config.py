"""Load model choices shared by the suite and single-model runner."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config.json"
MODEL_TIERS = ("lightweight", "medium", "complex")
TIERS = tuple(tier.title() for tier in MODEL_TIERS)


def load_models(path=DEFAULT_CONFIG):
    """Return validated model IDs in lightweight, medium, complex order."""
    path = Path(path).expanduser()
    config = json.loads(path.read_text(encoding="utf-8"))
    models = config.get("models") if isinstance(config, dict) else None
    if not isinstance(models, dict) or set(models) != set(MODEL_TIERS):
        raise ValueError(f"{path}: models must contain lightweight, medium and complex")
    ordered = [models[tier] for tier in MODEL_TIERS]
    if any(not isinstance(model, str) or not model.strip() or model != model.strip() for model in ordered):
        raise ValueError(f"{path}: each model must be a nonempty model ID or local directory without surrounding whitespace")
    if len(set(ordered)) != len(ordered):
        raise ValueError(f"{path}: use three distinct models")
    return ordered
