"""Command-line entry point to produce a sample savings report."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .analytics import find_best_prices
from .data_loader import default_data_paths, load_price_data
from .report import build_report


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(description="Generate a grocery savings report from JSON fixtures.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "data" / "samples",
        help="Directory containing retailer JSON files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = parse_args()
    args = parser.parse_args(argv)

    data_paths = default_data_paths(args.data_dir)
    if not data_paths:
        raise SystemExit(f"No data files found in {args.data_dir}")

    items = load_price_data(data_paths)
    recommendations = find_best_prices(items)
    report = build_report(items, recommendations)
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
