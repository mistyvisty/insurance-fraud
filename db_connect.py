import os
import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    host = os.getenv("DB_HOST", "localhost")
    db   = os.getenv("DB_NAME", "insurance_fraud")
    user = os.getenv("DB_USER", "preeti")
    pw   = os.getenv("DB_PASSWORD", "fraud123")
    return create_engine(f"postgresql://{user}:{pw}@{host}:5432/{db}")

def run_query(sql: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn)