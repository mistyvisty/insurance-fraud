import pandas as pd
from sqlalchemy import create_engine
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "insurance_fraud")
DB_USER = os.getenv("DB_USER", "preeti")
DB_PASS = os.getenv("DB_PASSWORD", "fraud123")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

df = pd.read_csv("data/healthcare_fraud_detection.csv")

# Rename columns to lowercase
df.columns = [c.lower().replace(" ", "_") for c in df.columns]

df["claim_submission_date"] = pd.to_datetime(df["claim_submission_date"])

df.to_sql("claims", engine, if_exists="append", index=False)
print(f"✅ Seeded {len(df)} rows into PostgreSQL!")