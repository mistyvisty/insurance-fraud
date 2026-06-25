# 1. KPI Overview
KPI = """
SELECT
    COUNT(*)                                        AS total_claims,
    SUM(is_fraud)                                   AS fraud_cases,
    ROUND(AVG(is_fraud)*100, 2)                     AS fraud_rate_pct,
    ROUND(SUM(claim_amount)::numeric, 2)            AS total_claimed,
    ROUND(SUM(approved_amount)::numeric, 2)         AS total_approved,
    ROUND(SUM(claim_amount - approved_amount)::numeric, 2) AS total_gap
FROM claims;
"""

# 2. Top fraudulent providers (window function)
TOP_FRAUD_PROVIDERS = """
SELECT
    provider_id,
    provider_specialty,
    COUNT(*)                            AS total_claims,
    SUM(is_fraud)                       AS fraud_claims,
    ROUND(AVG(is_fraud)*100, 2)         AS fraud_rate_pct,
    ROUND(SUM(claim_amount)::numeric,2) AS total_amount
FROM claims
GROUP BY provider_id, provider_specialty
HAVING COUNT(*) >= 5
ORDER BY fraud_rate_pct DESC
LIMIT 15;
"""

# 3. Fraud by specialty (CTE)
FRAUD_BY_SPECIALTY = """
WITH specialty_stats AS (
    SELECT
        provider_specialty,
        COUNT(*)                    AS total_claims,
        SUM(is_fraud)               AS fraud_claims,
        ROUND(AVG(is_fraud)*100,2)  AS fraud_rate_pct,
        ROUND(AVG(claim_amount)::numeric, 2) AS avg_claim
    FROM claims
    GROUP BY provider_specialty
)
SELECT * FROM specialty_stats
ORDER BY fraud_rate_pct DESC;
"""

# 4. Monthly fraud trend
MONTHLY_TREND = """
SELECT
    TO_CHAR(claim_submission_date, 'YYYY-MM') AS month,
    COUNT(*)                                   AS total_claims,
    SUM(is_fraud)                              AS fraud_cases,
    ROUND(AVG(is_fraud)*100, 2)                AS fraud_rate_pct
FROM claims
GROUP BY month
ORDER BY month;
"""

# 5. Fraud by state
FRAUD_BY_STATE = """
SELECT
    patient_state,
    COUNT(*)                        AS total_claims,
    SUM(is_fraud)                   AS fraud_cases,
    ROUND(AVG(is_fraud)*100, 2)     AS fraud_rate_pct
FROM claims
GROUP BY patient_state
ORDER BY fraud_cases DESC;
"""

# 6. Fraud by insurance type
FRAUD_BY_INSURANCE = """
SELECT
    insurance_type,
    COUNT(*)                        AS total_claims,
    SUM(is_fraud)                   AS fraud_cases,
    ROUND(AVG(is_fraud)*100, 2)     AS fraud_rate_pct,
    ROUND(AVG(claim_amount)::numeric, 2) AS avg_claim_amount
FROM claims
GROUP BY insurance_type
ORDER BY fraud_rate_pct DESC;
"""

# 7. High risk claims — CTE + window function
HIGH_RISK_CLAIMS = """
WITH provider_fraud_rate AS (
    SELECT
        provider_id,
        ROUND(AVG(is_fraud)*100, 2) AS provider_fraud_rate,
        RANK() OVER (ORDER BY AVG(is_fraud) DESC) AS fraud_rank
    FROM claims
    GROUP BY provider_id
)
SELECT
    c.claim_id,
    c.provider_id,
    c.claim_amount,
    c.provider_specialty,
    c.patient_state,
    p.provider_fraud_rate,
    p.fraud_rank
FROM claims c
JOIN provider_fraud_rate p ON c.provider_id = p.provider_id
WHERE c.is_fraud = 1
ORDER BY c.claim_amount DESC
LIMIT 20;
"""

# 8. Claim amount — fraud vs legit comparison
AMOUNT_COMPARISON = """
SELECT
    CASE WHEN is_fraud = 1 THEN 'Fraudulent' ELSE 'Legitimate' END AS claim_type,
    COUNT(*)                                    AS total_claims,
    ROUND(AVG(claim_amount)::numeric, 2)        AS avg_claim,
    ROUND(MIN(claim_amount)::numeric, 2)        AS min_claim,
    ROUND(MAX(claim_amount)::numeric, 2)        AS max_claim,
    ROUND(SUM(claim_amount)::numeric, 2)        AS total_amount
FROM claims
GROUP BY is_fraud;
"""

# 9. Visit type + chronic condition risk
RISK_FACTORS = """
SELECT
    visit_type,
    chronic_condition_flag,
    COUNT(*)                        AS total_claims,
    SUM(is_fraud)                   AS fraud_cases,
    ROUND(AVG(is_fraud)*100, 2)     AS fraud_rate_pct
FROM claims
GROUP BY visit_type, chronic_condition_flag
ORDER BY fraud_rate_pct DESC;
"""

# 10. Provider claims volume vs fraud (window function)
PROVIDER_VOLUME_RISK = """
SELECT
    provider_id,
    provider_specialty,
    COUNT(*) AS total_claims,
    SUM(is_fraud) AS fraud_claims,
    ROUND(AVG(is_fraud)*100,2) AS fraud_rate_pct,
    NTILE(4) OVER (ORDER BY COUNT(*)) AS volume_quartile
FROM claims
GROUP BY provider_id, provider_specialty
ORDER BY fraud_claims DESC
LIMIT 20;
"""