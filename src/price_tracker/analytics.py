"""Analytical helpers for identifying buying opportunities."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Dict, Iterable, List

from .data_loader import ItemPrice


@dataclass
class Recommendation:
    item: ItemPrice
    reason: str
    priority: str  # low, medium, high


def _seasonal_factor(category: str, today: date) -> float:
    """Return a seasonal multiplier (<1 encourages buying) for certain categories."""

    month = today.month
    category = category.lower()
    # Cheaper after main season: holiday decor after January, seasonal produce in-season
    if category in {"holiday", "decor"}:
        return 0.8 if month in {1, 2} else 1.0
    if category in {"produce", "fruit"}:
        # Assume peak freshness/price in late summer/early fall
        return 0.9 if month in {8, 9, 10} else 1.05
    return 1.0


def find_best_prices(items: Iterable[ItemPrice], today: date | None = None) -> List[Recommendation]:
    """Return recommendations for items priced meaningfully below MSRP.

    A discount above 10% is treated as a strong buy, 5-10% as a moderate buy.
    Seasonal factors slightly adjust the effective discount.
    """

    today = today or date.today()
    best_by_name: Dict[str, ItemPrice] = {}

    for item in items:
        current_best = best_by_name.get(item.name)
        if current_best is None or item.price < current_best.price:
            best_by_name[item.name] = item

    recommendations: List[Recommendation] = []
    for best in best_by_name.values():
        factor = _seasonal_factor(best.category, today)
        adjusted_discount = round(best.discount_pct * factor, 2)
        if adjusted_discount >= 10:
            priority = "high"
            reason = f"Effective {adjusted_discount}% off after seasonal factors; strong buy."
        elif adjusted_discount >= 5:
            priority = "medium"
            reason = f"Effective {adjusted_discount}% off after seasonal factors; good time to buy."
        else:
            continue
        recommendations.append(Recommendation(item=best, reason=reason, priority=priority))

    # Stable ordering: highest discount first, then name
    recommendations.sort(key=lambda rec: (-rec.item.discount_pct, rec.item.name))
    return recommendations


def summarize_by_category(items: Iterable[ItemPrice]) -> Dict[str, float]:
    """Compute average price per category to help spot trends."""

    totals: Dict[str, float] = defaultdict(float)
    counts: Dict[str, int] = defaultdict(int)
    for item in items:
        totals[item.category] += item.price
        counts[item.category] += 1
    return {cat: round(totals[cat] / counts[cat], 2) for cat in totals}
