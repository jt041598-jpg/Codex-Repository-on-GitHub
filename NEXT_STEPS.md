# Path to a production-ready household savings assistant

This prototype only loads local JSON fixtures. The checklist below outlines the work needed to ship a usable daily savings assistant that watches real retailers, personalizes alerts, and delivers email reports.

## Data ingestion
- Add connectors for multiple retailers (e.g., grocery chains, warehouse clubs, Amazon/Target) using APIs or lightweight scrapers; normalize to the existing `ItemPrice` schema.
- Implement scheduleable crawlers (cron/Airflow) that refresh prices daily and store raw responses for debugging.
- Add rate-limit and captcha-safe scraping patterns where APIs are unavailable; centralize user-agents, retries, and backoff.

## Storage and history
- Persist normalized prices to a database (SQLite for local testing, Postgres in production) with item IDs, retailer IDs, timestamps, and currency/unit metadata.
- Track price history to compute rolling averages, seasonality curves, and detect regressions in scraper output.
- Introduce canonical product matching (SKU/UPC, fuzzy name match) so offers from different retailers map to the same item.

## Analytics and recommendations
- Replace the static seasonal factor with a learned or rules-based model that uses historical price trends and holiday calendars.
- Support household preferences: watchlists, brand exclusions, package-size normalization, and budget thresholds.
- Implement stock-awareness flags (e.g., low inventory, online-only) and shipping/fees adjustments for true delivered cost.

## Reporting and delivery
- Generate multi-channel output: email (plain text + HTML), optional SMS push for high-priority deals, and a daily CSV/JSON export.
- Add templated, localized report rendering with per-recipient preferences and unsubscribe links.
- Integrate with an SMTP provider (e.g., SES, SendGrid) and add smoke tests to verify delivery.

## Operations and quality
- Add automated tests for loaders, matching, analytics, and report rendering; include fixtures for each retailer connector.
- Provide configuration via environment variables and `.env` files; document secrets management.
- Containerize the worker (ingestion + analytics) and scheduler; add health checks, logging, and metrics (latency, success rate, coverage).
- Set up CI to run formatting, linting, type checks, and the test suite on each commit.

## How to pilot quickly
- Start with 2–3 retailers that have stable public APIs or HTML structures.
- Seed a small watchlist (toilet paper, detergent, apples, holiday decor) and run nightly to validate data quality.
- Compare alerts against real weekly ads to tune thresholds before expanding coverage.
