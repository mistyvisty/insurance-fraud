import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_connect import get_engine
from queries import (
    KPI,
    TOP_FRAUD_PROVIDERS,
    FRAUD_BY_SPECIALTY,
    MONTHLY_TREND,
    FRAUD_BY_STATE,
    FRAUD_BY_INSURANCE,
    HIGH_RISK_CLAIMS,
    AMOUNT_COMPARISON,
    RISK_FACTORS,
    PROVIDER_VOLUME_RISK
)

st.set_page_config(
    page_title="Healthcare Fraud Detection",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Insurance Fraud Detection Dashboard")
st.markdown("---")

engine = get_engine()

# --- KPI Cards ---
st.subheader("📊 Overview")
overview = pd.read_sql(KPI, engine)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Claims", f"{int(overview['total_claims'][0]):,}")
col2.metric("Fraud Cases", f"{int(overview['fraud_cases'][0]):,}")
col3.metric("Fraud Rate", f"{float(overview['fraud_rate_pct'][0]):.2f}%")
col4.metric("Total Claimed", f"${float(overview['total_claimed'][0]):,.0f}")
col5.metric("Total Gap", f"${float(overview['total_gap'][0]):,.0f}")

st.markdown("---")

# --- Row 1: Specialty + Insurance ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏨 Fraud by Provider Specialty")
    df = pd.read_sql(FRAUD_BY_SPECIALTY, engine)
    fig = px.bar(df, x="fraud_claims", y="provider_specialty",
                 orientation="h", color="fraud_rate_pct",
                 color_continuous_scale="Reds",
                 labels={"fraud_claims": "Fraud Claims", "provider_specialty": "Specialty"})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💳 Fraud by Insurance Type")
    df2 = pd.read_sql(FRAUD_BY_INSURANCE, engine)
    fig2 = px.pie(df2, names="insurance_type", values="fraud_cases",
                  hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- Row 2: State Map + Amount Comparison ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗺️ Fraud by State")
    df3 = pd.read_sql(FRAUD_BY_STATE, engine)
    fig3 = px.choropleth(df3, locations="patient_state",
                         locationmode="USA-states",
                         color="fraud_cases",
                         scope="usa",
                         color_continuous_scale="Reds",
                         labels={"fraud_cases": "Fraud Cases"})
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("💰 Fraud vs Legitimate Claim Amounts")
    df4 = pd.read_sql(AMOUNT_COMPARISON, engine)
    fig4 = px.bar(df4, x="claim_type", y="avg_claim",
                  color="claim_type",
                  color_discrete_map={"Fraudulent": "#e63946", "Legitimate": "#2a9d8f"},
                  labels={"avg_claim": "Avg Claim Amount", "claim_type": "Claim Type"})
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --- Row 3: Risk Factors ---
st.subheader("⚠️ Fraud by Visit Type & Chronic Condition")
df5 = pd.read_sql(RISK_FACTORS, engine)
fig5 = px.bar(df5, x="visit_type", y="fraud_rate_pct",
              color="chronic_condition_flag",
              barmode="group",
              labels={"fraud_rate_pct": "Fraud Rate %", "visit_type": "Visit Type",
                      "chronic_condition_flag": "Chronic Condition"})
fig5.update_layout(height=400)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# --- Monthly Trend ---
st.subheader("📈 Monthly Fraud Trend")
df6 = pd.read_sql(MONTHLY_TREND, engine)
df6["month"] = df6["month"].astype(str)
fig6 = px.line(df6, x="month", y="fraud_cases",
               markers=True, color_discrete_sequence=["#e63946"],
               labels={"fraud_cases": "Fraud Cases", "month": "Month"})
fig6.update_layout(height=350)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# --- High Risk Claims Table ---
st.subheader("🚨 High Risk Claims")
df7 = pd.read_sql(HIGH_RISK_CLAIMS, engine)
st.dataframe(df7, use_container_width=True)

st.markdown("---")

# --- Top Fraud Providers ---
st.subheader("👤 Top Fraudulent Providers")
df8 = pd.read_sql(TOP_FRAUD_PROVIDERS, engine)
fig8 = px.bar(df8, x="fraud_rate_pct", y="provider_id",
              orientation="h", color="fraud_rate_pct",
              color_continuous_scale="Reds",
              labels={"fraud_rate_pct": "Fraud Rate %", "provider_id": "Provider ID"})
fig8.update_layout(height=500)
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# --- Provider Volume Risk ---
st.subheader("📦 Provider Volume vs Fraud Risk")
df9 = pd.read_sql(PROVIDER_VOLUME_RISK, engine)
fig9 = px.scatter(df9, x="total_claims", y="fraud_rate_pct",
                  size="fraud_claims", color="provider_specialty",
                  hover_data=["provider_id"],
                  labels={"total_claims": "Total Claims", "fraud_rate_pct": "Fraud Rate %"})
fig9.update_layout(height=450)
st.plotly_chart(fig9, use_container_width=True)