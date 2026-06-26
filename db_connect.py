import os
import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    url = os.getenv("DATABASE_URL")
    return create_engine(url)

def run_query(sql: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn)
