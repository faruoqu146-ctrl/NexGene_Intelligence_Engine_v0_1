"""Production/dev entrypoint wrapper.

- Normalizes postgres:// -> postgresql:// before engines are created
- Imports main (create_all runs there)
- Runs additive column migrations for existing DBs

Use: uvicorn backend.app.bootstrap:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import os


def _normalize_db_urls() -> None:
    for key in ("DATABASE_URL", "CLINICAL_DATABASE_URL", "GENOMIC_DATABASE_URL"):
        val = os.environ.get(key)
        if val and val.startswith("postgres://"):
            os.environ[key] = "postgresql://" + val[len("postgres://") :]


_normalize_db_urls()

# Import after URL normalization so create_engine sees postgresql://
from backend.app import main as main_module  # noqa: E402
from backend.app.migrate_schema import run_lightweight_migrations  # noqa: E402

run_lightweight_migrations(main_module.engine)

app = main_module.app
