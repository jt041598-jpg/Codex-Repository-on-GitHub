"""Helpers to format a daily savings report."""

from __future__ import annotations

from datetime import date
from typing import Iterable, List

from .analytics import Recommendation, summarize_by_category
from .data_loader import ItemPrice


def build_report(items: Iterable[ItemPrice], recommendations: List[Recommendation], *, today: date | None = None) -> str:
    """Render a human-friendly text report."""

    today = today or date.today()
    lines: List[str] = []
    lines.append(f"Daily Savings Report for {today:%Y-%m-%d}")
    lines.append("=" * 36)
    lines.append("")

    if recommendations:
        lines.append("Top Buy Suggestions:")
        for rec in recommendations:
            item = rec.item
            lines.append(
                f"- {item.name} at {item.retailer}: ${item.price:.2f} ({item.discount_pct}% off MSRP; {rec.reason})"
            )
            if item.notes:
                lines.append(f"  Notes: {item.notes}")
    else:
        lines.append("No items meet the buy-now threshold today.")
    lines.append("")

    lines.append("Category Averages (price per unit):")
    for category, avg in summarize_by_category(items).items():
        lines.append(f"- {category}: ${avg:.2f}")

    return "\n".join(lines)
