"""Snowflake connection helper. Reads credentials from environment (.env)."""
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    required = ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}. Copy .env.example to .env.")

    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE", "PC_DBT_DB"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
    )
