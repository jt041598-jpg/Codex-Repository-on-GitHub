# Household Savings Report Prototype

This lightweight prototype shows how to generate a daily savings report for groceries and home supplies. It loads sample retailer price files, spots the best discounts, and formats a text report suitable for email delivery.

## Running the sample

```
python -m src.price_tracker.main
```

Use `--data-dir` to point at a different directory of retailer JSON exports if you have them locally.

## How it works

- `data/samples/` contains mock retailer exports for toilet paper, detergent, apples, and an off-season artificial Christmas tree.
- `src/price_tracker/data_loader.py` reads the JSON files into structured `ItemPrice` records.
- `src/price_tracker/analytics.py` evaluates the best offer per item and adjusts recommendations with simple seasonal hints (for example, holiday decor is scored favorably after the holidays, and fruit prices trend higher out of season).
- `src/price_tracker/report.py` formats a human-readable report with buy-now suggestions and category averages.
- `src/price_tracker/main.py` wires everything together for a command-line run; in production you could connect this to an emailer or scheduler (e.g., cron, Airflow) to send the report daily.

## Extending to real-world data

To track more retailers, add JSON exports under `data/` with `retailer`, `name`, `category`, `price`, and `msrp` fields. The loader and analytics modules are pure Python and can be integrated with web scrapers or API clients that keep the same schema.

## Next steps toward a production system

See [`NEXT_STEPS.md`](NEXT_STEPS.md) for a concise checklist that covers live data ingestion, persistent storage, smarter recommendations, and automated delivery of daily reports.
