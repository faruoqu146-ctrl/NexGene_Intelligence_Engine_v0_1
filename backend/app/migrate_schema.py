"""Lightweight additive schema upgrades for existing DBs (SQLite + Postgres).

create_all only creates missing tables; it does not add columns to existing ones.
This module fills that gap for columns introduced after early pilot DBs.
"""
from __future__ import annotations

from sqlalchemy import inspect, text as sql_text


def _add_column_if_missing(conn, table: str, column: str, ddl: str) -> None:
    insp = inspect(conn)
    if table not in set(insp.get_table_names()):
        return
    existing = {c["name"] for c in insp.get_columns(table)}
    if column in existing:
        return
    conn.execute(sql_text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))


def run_lightweight_migrations(engine) -> None:
    with engine.begin() as conn:
        _add_column_if_missing(conn, "users", "email_verified", "email_verified BOOLEAN DEFAULT FALSE")
        _add_column_if_missing(conn, "users", "google_sub", "google_sub VARCHAR(255)")
        _add_column_if_missing(conn, "users", "ai_analysis_enabled", "ai_analysis_enabled BOOLEAN DEFAULT FALSE")
        _add_column_if_missing(conn, "profiles", "location_city", "location_city VARCHAR(160)")
        _add_column_if_missing(conn, "profiles", "live_context_enabled", "live_context_enabled BOOLEAN DEFAULT TRUE")
        try:
            conn.execute(
                sql_text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_google_sub_unique "
                    "ON users(google_sub) WHERE google_sub IS NOT NULL"
                )
            )
        except Exception:
            # Older engines / permission edge cases — non-fatal
            pass
