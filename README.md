# Healthcare Insurance Fraud Detection Dashboard

## Overview
A full-stack fraud detection dashboard that analyzes 10,000 healthcare insurance claims to identify fraudulent patterns using SQL analytics and interactive visualizations.

## Key Stats
- Total Claims: 10,000
- Fraud Cases: 829 (8.29%)
- Total Claimed: $5,728,044
- Fraud Gap: $972,902

## Tech Stack
- PostgreSQL 15 — window functions and CTEs
- Docker + Docker Compose — containerized setup
- Python — data seeding and querying
- Streamlit — interactive dashboard
- Plotly — charts and visualizations

## How to Run
docker-compose up --build
Then open http://localhost:8501

## Dashboard Features
- KPI Overview (fraud rate, total claims, amounts)
- Fraud by Provider Specialty
- Fraud by Insurance Type
- Fraud by State (USA map)
- Fraud vs Legitimate Amount Comparison
- Risk Factors by Visit Type and Chronic Condition
- Monthly Fraud Trend
- High Risk Claims Table
- Top Fraudulent Providers
- Provider Volume vs Fraud Risk

Built by Preeti Bhardwaj — github.com/mistyvisty
