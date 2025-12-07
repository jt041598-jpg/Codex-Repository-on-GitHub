"""Helpers for loading price data from local JSON fixtures.

This module is intentionally file-system only to make it safe in environments
without network access. In a real deployment, `load_price_data` could be
extended to fetch from APIs or scrapers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class ItemPrice:
    """Represents a single price observation for an item at a retailer."""

    retailer: str
    name: str
    category: str
    price: float
    unit: str
    msrp: float
    start_date: str
    end_date: str | None
    notes: str | None = None

    @property
    def discount_pct(self) -> float:
        """Percentage discount relative to MSRP."""

        if self.msrp == 0:
            return 0
        return round((1 - self.price / self.msrp) * 100, 2)


def load_price_data(paths: Iterable[Path]) -> List[ItemPrice]:
    """Load item prices from JSON files.

    Each file should contain an array of objects with fields matching ``ItemPrice``.
    Missing optional fields default to ``None``.
    """

    items: List[ItemPrice] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for row in data:
            items.append(
                ItemPrice(
                    retailer=row["retailer"],
                    name=row["name"],
                    category=row.get("category", "uncategorized"),
                    price=float(row["price"]),
                    unit=row.get("unit", "unit"),
                    msrp=float(row.get("msrp", row["price"])),
                    start_date=row.get("start_date", ""),
                    end_date=row.get("end_date"),
                    notes=row.get("notes"),
                )
            )
    return items


def default_data_paths(base_dir: Path) -> List[Path]:
    """Return JSON fixture paths under ``base_dir`` for convenience."""

    return sorted(base_dir.glob("*.json"))
