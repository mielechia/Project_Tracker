"""
Migration: Recalculate all project USD values using ExchangeRate-API key.

How to use:
1) Put this file in the same folder as your database.
2) Set your API key:
   macOS/Linux:
      export EXCHANGERATE_API_KEY="your_api_key_here"
   Windows PowerShell:
      setx EXCHANGERATE_API_KEY "your_api_key_here"

3) Run:
      python migrate_exchange_rates_to_api.py --db Project_Tracker_v3_accurate_users_pm.db

What it does:
- Backs up your database first.
- Ensures USD/exchange-rate columns exist.
- For every project, fetches currency -> USD rate using your API key.
- Recalculates:
    f_revenue_usd
    f_cost_usd
    f_nprofit_usd
    exchange_rate
    exchange_rate_date
    exchange_rate_source
- Uses the same stored original values:
    f_currency
    f_revenue
    f_cost
    f_nprofit
"""

import argparse
import os
import shutil
import sqlite3
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Dict

import requests


API_ENV_NAME = "EXCHANGERATE_API_KEY"
API_SOURCE = "ExchangeRate-API"
API_BASE_URL = "https://v6.exchangerate-api.com/v6"


def ensure_columns(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(projects)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    columns_to_add = {
        "f_revenue_usd": "FLOAT",
        "f_cost_usd": "FLOAT",
        "f_nprofit_usd": "FLOAT",
        "exchange_rate": "FLOAT",
        "exchange_rate_date": "TEXT",
        "exchange_rate_source": "TEXT",
    }

    for column_name, column_type in columns_to_add.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE projects ADD COLUMN {column_name} {column_type}")

    conn.commit()


def fetch_rate_to_usd(currency: str, api_key: str, cache: Dict[str, float]) -> float:
    currency = (currency or "").strip().upper()

    if not currency:
        raise ValueError("Missing currency")

    if currency == "USD":
        return 1.0

    if currency in cache:
        return cache[currency]

    url = f"{API_BASE_URL}/{api_key}/pair/{currency}/USD"
    response = requests.get(url, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(f"API HTTP {response.status_code}: {response.text[:300]}")

    data = response.json()

    if data.get("result") != "success":
        raise RuntimeError(f"API error for {currency}: {data}")

    rate = float(data["conversion_rate"])
    cache[currency] = rate

    # Small pause to be gentle with the free API tier.
    time.sleep(0.15)

    return rate


def safe_float(value) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview updates without writing to database",
    )
    args = parser.parse_args()

    db_path = args.db
    api_key = os.getenv(API_ENV_NAME)

    if not api_key:
        raise SystemExit(
            f"Missing API key. Please set environment variable {API_ENV_NAME} first."
        )

    if not os.path.exists(db_path):
        raise SystemExit(f"Database not found: {db_path}")

    backup_path = db_path.replace(".db", f"_backup_before_api_rates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

    if not args.dry_run:
        shutil.copy2(db_path, backup_path)
        print(f"Backup created: {backup_path}")

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        ensure_columns(conn)

        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                db_id, p_name, f_currency, f_revenue, f_cost, f_nprofit
            FROM projects
            ORDER BY db_id
            """
        )
        projects = cursor.fetchall()

        rate_cache: Dict[str, float] = {}
        updated_count = 0
        skipped_count = 0
        error_rows = []

        now_kl = datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).isoformat()

        for project in projects:
            db_id = project["db_id"]
            currency = (project["f_currency"] or "").strip().upper()

            revenue = safe_float(project["f_revenue"])
            cost = safe_float(project["f_cost"])
            nprofit = safe_float(project["f_nprofit"])

            if nprofit is None and revenue is not None and cost is not None:
                nprofit = round(revenue - cost, 2)

            try:
                rate = fetch_rate_to_usd(currency, api_key, rate_cache)
            except Exception as exc:
                skipped_count += 1
                error_rows.append((db_id, project["p_name"], currency, str(exc)))
                continue

            revenue_usd = round(revenue * rate, 2) if revenue is not None else None
            cost_usd = round(cost * rate, 2) if cost is not None else None
            nprofit_usd = round(nprofit * rate, 2) if nprofit is not None else None

            if args.dry_run:
                print(
                    f"[DRY RUN] DB ID {db_id}: {currency} rate={rate} "
                    f"profit={nprofit} -> USD {nprofit_usd}"
                )
            else:
                cursor.execute(
                    """
                    UPDATE projects
                    SET 
                        f_currency = ?,
                        f_revenue_usd = ?,
                        f_cost_usd = ?,
                        f_nprofit_usd = ?,
                        exchange_rate = ?,
                        exchange_rate_date = ?,
                        exchange_rate_source = ?
                    WHERE db_id = ?
                    """,
                    (
                        currency,
                        revenue_usd,
                        cost_usd,
                        nprofit_usd,
                        rate,
                        now_kl,
                        API_SOURCE,
                        db_id,
                    ),
                )

            updated_count += 1

        if not args.dry_run:
            conn.commit()

    print("\nMigration completed.")
    print(f"Projects processed: {len(projects)}")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Unique currencies fetched: {sorted(rate_cache.keys())}")

    if error_rows:
        print("\nSkipped rows:")
        for row in error_rows[:30]:
            print(f"- DB ID {row[0]} | {row[1]} | {row[2]} | {row[3]}")
        if len(error_rows) > 30:
            print(f"... and {len(error_rows) - 30} more")


if __name__ == "__main__":
    main()
