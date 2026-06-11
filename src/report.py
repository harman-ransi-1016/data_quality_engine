"""Format check results into a console summary table."""
from tabulate import tabulate


def render(results):
    rows = [
        ["PASS" if r.passed else "FAIL", r.table.split(".")[-1], r.name, r.detail]
        for r in results
    ]
    table = tabulate(rows, headers=["status", "table", "check", "detail"], tablefmt="github")
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    summary = f"\n{passed} passed, {failed} failed, {len(results)} total"
    return table + "\n" + summary
