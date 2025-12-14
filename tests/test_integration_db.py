import os
import pytest


pytestmark = pytest.mark.skipif(
    not (os.getenv("DB_USER") and os.getenv("DB_PASS") and os.getenv("DB_DSN")),
    reason="Oracle DB credentials not configured in environment"
)


def test_db_connection():
    # Simple smoke test to verify that the DB connection can be established
    from db.connection import get_connection

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    r = cur.fetchone()
    cur.close()
    conn.close()

    assert r is not None
