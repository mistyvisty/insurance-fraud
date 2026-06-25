CREATE TABLE IF NOT EXISTS claims (
    provider_id                           VARCHAR(20),
    claim_id                              VARCHAR(20) PRIMARY KEY,
    patient_age                           INTEGER,
    patient_gender                        VARCHAR(10),
    diagnosis_code                        VARCHAR(20),
    procedure_code                        INTEGER,
    claim_amount                          NUMERIC(10,2),
    approved_amount                       NUMERIC(10,2),
    insurance_type                        VARCHAR(50),
    claim_submission_date                 DATE,
    days_between_service_and_claim        INTEGER,
    number_of_claims_per_provider_monthly INTEGER,
    provider_specialty                    VARCHAR(100),
    patient_state                         VARCHAR(5),
    claim_status                          VARCHAR(50),
    is_fraud                              INTEGER,
    length_of_stay                        INTEGER,
    visit_type                            VARCHAR(50),
    chronic_condition_flag                INTEGER,
    prior_visits_12m                      NUMERIC(5,1)
);

CREATE INDEX idx_provider  ON claims(provider_id);
CREATE INDEX idx_fraud     ON claims(is_fraud);
CREATE INDEX idx_specialty ON claims(provider_specialty);
CREATE INDEX idx_state     ON claims(patient_state);
CREATE INDEX idx_date      ON claims(claim_submission_date);