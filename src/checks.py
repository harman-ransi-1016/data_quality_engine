"""One function per check type. Each runs a SQL query and returns a Result.

A check PASSES when its query returns 0 offending rows (or meets a threshold),
mirroring how dbt tests work (a test returns failing rows).
"""
from dataclasses import dataclass


@dataclass
class Result:
    name: str
    table: str
    passed: bool
    detail: str


def _scalar(conn, sql):
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchone()[0]
    finally:
        cur.close()


def check_not_null(conn, c):
    n = _scalar(conn, f"SELECT count(*) FROM {c['table']} WHERE {c['column']} IS NULL")
    return Result(f"not_null({c['column']})", c["table"], n == 0, f"{n} null(s)")


def check_unique(conn, c):
    sql = (
        f"SELECT count(*) FROM (SELECT {c['column']} FROM {c['table']} "
        f"GROUP BY {c['column']} HAVING count(*) > 1)"
    )
    n = _scalar(conn, sql)
    return Result(f"unique({c['column']})", c["table"], n == 0, f"{n} duplicated value(s)")


def check_accepted_values(conn, c):
    allowed = ", ".join(f"'{v}'" for v in c["values"])
    sql = f"SELECT count(*) FROM {c['table']} WHERE {c['column']} NOT IN ({allowed})"
    n = _scalar(conn, sql)
    return Result(f"accepted_values({c['column']})", c["table"], n == 0, f"{n} unexpected value(s)")


def check_row_count_min(conn, c):
    n = _scalar(conn, f"SELECT count(*) FROM {c['table']}")
    return Result(f"row_count_min({c['min']})", c["table"], n >= c["min"], f"{n} rows")


def check_freshness(conn, c):
    sql = (
        f"SELECT datediff('hour', max({c['column']}), current_timestamp) FROM {c['table']}"
    )
    age = _scalar(conn, sql)
    age = age if age is not None else 10**9
    ok = age <= c["max_age_hours"]
    return Result(f"freshness({c['column']})", c["table"], ok, f"{age}h old (limit {c['max_age_hours']}h)")

def check_max_value(conn, c):
    n = _scalar(conn, f"SELECT count(*) FROM {c['table']} WHERE {c['column']} > {c['max']}")
    return Result(f"max_value({c['column']}<={c['max']})", c["table"], n == 0, f"{n} row(s) over {c['max']}")

REGISTRY = {
    "not_null": check_not_null,
    "unique": check_unique,
    "accepted_values": check_accepted_values,
    "row_count_min": check_row_count_min,
    "freshness": check_freshness,
    "max_value": check_max_value,        # <-- add this
}