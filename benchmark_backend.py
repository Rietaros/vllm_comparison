"""Backend selection and resource budgets without importing GPU runtimes."""
from __future__ import annotations

import platform

BACKENDS = ("auto", "metal", "cuda")
CACHE_POLICIES = {"metal": "physical-budget-to-metal-with-block-override-v1",
                  "cuda": "vram-budget-with-block-override-v1"}


def resolve_backend(requested="auto"):
    if requested != "auto":
        return requested
    return "metal" if platform.system() == "Darwin" else "cuda"


def add_backend_arguments(parser):
    parser.add_argument("--backend", choices=BACKENDS, default="auto",
                        help="auto selects Metal on macOS and NVIDIA CUDA on Linux")


def device_memory_budget(hardware, fraction=None, budget_gib=None):
    """Plan against unified RAM on Metal, selected GPU VRAM on CUDA."""
    cuda = hardware.get("backend") == "cuda"
    capacity = hardware["gpu_memory_bytes"] if cuda else hardware["memory_bytes"]
    if budget_gib is None and fraction is None:
        budget_gib = 10.0
    requested = int(budget_gib * 1024**3) if budget_gib is not None else int(capacity * fraction)
    limit = capacity if cuda else hardware.get("metal_device", {}).get("max_recommended_working_set_size", capacity)
    # Leave room for the CUDA context and other users of this GPU. This is a
    # planning guard; vLLM still performs its own free-memory check at startup.
    effective = min(requested, int(capacity * .95) if cuda else capacity, limit)
    return {"requested_bytes": requested, "effective_bytes": effective,
            "device_limit_bytes": limit, "metal_limit_bytes": limit if not cuda else None,
            "backend_memory_fraction": effective / limit,
            "source": "GiB" if budget_gib is not None else ("VRAM fraction" if cuda else "RAM fraction")}


def hardware_description(hardware):
    if hardware.get("backend") == "cuda":
        return (f"{hardware.get('gpu_name', 'NVIDIA GPU (not detected)')}, "
                f"{hardware.get('gpu_memory_bytes', 0) / 1024**3:.1f} GiB GPU VRAM, "
                f"{hardware['os']} {hardware['os_version']}. Backend: NVIDIA CUDA")
    return (f"{hardware.get('chip', hardware['architecture'])}, "
            f"{hardware.get('memory_bytes', 0) / 1024**3:.0f} GiB unified RAM, "
            f"{hardware['os']} {hardware['os_version']}. Backend: vLLM-Metal")
