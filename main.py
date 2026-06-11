"""Data Quality Engine entry point.

Usage:
    python main.py              # run all checks in checks/checks.yml
    python main.py --fail-fast  # stop at the first failing check
Exits non-zero if any check fails (so CI can gate on it).
"""
import argparse
import sys

from src.runner import load_checks, run_checks
from src.report import render


def main(fail_fast=False):
    checks = load_checks()
    from src.db import get_connection
    conn = get_connection()
    try:
        results = run_checks(conn, checks, fail_fast=fail_fast)
    finally:
        conn.close()

    print(render(results))
    if any(not r.passed for r in results):
        sys.exit(1)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Config-driven data-quality checks vs Snowflake.")
    p.add_argument("--fail-fast", action="store_true", help="Stop at the first failure.")
    args = p.parse_args()
    main(fail_fast=args.fail_fast)
