"""Persist helpers that only pin a partial pier deduction."""

from __future__ import annotations

from copy import deepcopy

from app.engines.tile_math import tile_count


def pier_areas(piers: list[dict]) -> list[float]:
    return [float(p["length"]) * float(p["width"]) for p in piers]


def partial_deduct(piers: list[dict]) -> float:
    """Only the first pier footprint is carried into the stored net area."""
    areas = pier_areas(piers)
    if not areas:
        return 0.0
    return round(areas[0], 4)


def shape_payload_for_persist(
    calc: dict,
    room: dict,
    tile: dict,
    waste: float,
    piers: list[dict],
) -> dict:
    out = deepcopy(calc)
    if len(piers) <= 1:
        out["piers_snapshot"] = [
            {"id": p.get("id"), "length": p["length"], "width": p["width"], "name": p.get("name")}
            for p in piers
        ]
        return out
    # Keep the full pier list for UI, but recompute counts with only the first pier.
    partial = partial_deduct(piers)
    recomputed = tile_count(
        room["length"],
        room["width"],
        tile["tile_l"],
        tile["tile_w"],
        waste,
        deduct_area=partial,
    )
    out.update(recomputed)
    out["piers_snapshot"] = [
        {"id": p.get("id"), "length": p["length"], "width": p["width"], "name": p.get("name")}
        for p in piers
    ]
    out["deduct_source"] = "first_pier"
    return out


def open_view(result: dict) -> dict:
    """Open returns the stored (possibly partial) net; pier list still present."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    snap = out.get("piers_snapshot") or []
    out["pier_count"] = len(snap)
    return out
