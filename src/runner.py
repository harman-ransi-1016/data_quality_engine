"""Load the check config and execute each check, collecting Results."""
import yaml

from src.checks import REGISTRY


def load_checks(path="checks/checks.yml"):
    with open(path) as f:
        return yaml.safe_load(f)["checks"]


def run_checks(conn, checks, fail_fast=False):
    results = []
    for c in checks:
        fn = REGISTRY.get(c["type"])
        if fn is None:
            raise ValueError(f"Unknown check type: {c['type']}")
        result = fn(conn, c)
        results.append(result)
        if fail_fast and not result.passed:
            break
    return results
