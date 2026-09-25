"""Persist helpers for pier (柱墩) deduction snapshots.

The stored payload must carry exactly the numbers the estimate response
returned: net area = gross - the footprint of *every* current pier, and
order_count derived from that net area. Nothing here recomputes against a
partial pier set, so a run opened later can never silently drop a pier or
deduct one twice.
"""

from __future__ import annotations

from copy import deepcopy


def pier_areas(piers: list[dict]) -> list[float]:
    return [float(p["length"]) * float(p["width"]) for p in piers]


def shape_payload_for_persist(calc: dict, piers: list[dict]) -> dict:
    """Attach the pier snapshot to the already fully-deducted calc result.

    ``calc`` comes from ``tile_count(deduct_area=sum(all pier footprints))``
    and is persisted unchanged; the snapshot only records which piers were
    present at write time for later display.
    """
    out = deepcopy(calc)
    out["piers_snapshot"] = [
        {"id": p.get("id"), "length": p["length"], "width": p["width"], "name": p.get("name")}
        for p in piers
    ]
    return out


def open_view(result: dict) -> dict:
    """Return the stored numbers unchanged (plus a pier_count convenience)."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    snap = out.get("piers_snapshot") or []
    out["pier_count"] = len(snap)
    return out
