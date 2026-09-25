"""Persist/open helpers: pin the full pier snapshot next to the computed result."""

from __future__ import annotations

from copy import deepcopy


def shape_payload_for_persist(calc: dict, piers: list[dict]) -> dict:
    """Store the computed result untouched (all piers deducted exactly once);
    the pier list rides along so the detail view can still show it."""
    out = deepcopy(calc)
    out["piers_snapshot"] = [
        {"id": p.get("id"), "length": p["length"], "width": p["width"], "name": p.get("name")}
        for p in piers
    ]
    return out


def open_view(result: dict) -> dict:
    """Open returns the stored net as written; pier list still present."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    snap = out.get("piers_snapshot") or []
    out["pier_count"] = len(snap)
    return out
