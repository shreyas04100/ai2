"""
Dataset Generator Script for Customer Churn Preprocessing Project
Generates a realistic synthetic customer churn dataset with deliberate real-world flaws:
- Missing values (NaNs and blank strings)
- Duplicate records
- Inconsistent categorical text values (e.g., casing/abbreviation inconsistencies)
- Numerical outliers (extreme positive/negative values)
- Data type mismatches (numerical columns formatted as strings)
- Redundant / uninformative columns for feature selection demonstrations
"""

import os
import numpy as np
import pandas as pd

def generate_raw_churn_dataset(seed: int = 42, num_records: int = 1200, output_path: str = "data/raw/customer_churn_raw.csv") -> pd.DataFrame:
    """
    Generates a synthetic dataset with realistic Telco Customer Churn properties and intentional flaws.
    """
    np.random.seed(seed)
    
    # 1. Base Customer IDs
    customer_ids = [f"CUST-{10000 + i}" for i in range(num_records)]
    
    # 2. Demographics & Account Info
    genders_clean = np.random.choice(["Male", "Female"], size=num_records, p=[0.49, 0.51])
    # Introduce inconsistent categorical encoding (female, F, M, Male, Female)
    genders_noisy = genders_clean.copy().astype(object)
    typo_indices_g = np.random.choice(num_records, size=50, replace=False)
    for idx in typo_indices_g:
        if genders_noisy[idx] == "Female":
            genders_noisy[idx] = np.random.choice(["female", "F"])
        else:
            genders_noisy[idx] = np.random.choice(["male", "M"])
            
    senior_citizen = np.random.choice([0, 1], size=num_records, p=[0.84, 0.16]).astype(object)
    partner = np.random.choice(["Yes", "No"], size=num_records, p=[0.48, 0.52]).astype(object)
    dependents = np.random.choice(["Yes", "No"], size=num_records, p=[0.30, 0.70]).astype(object)
    
    # 3. Service details
    tenure_months = np.random.randint(1, 73, size=num_records).astype(float)
    phone_service = np.random.choice(["Yes", "No"], size=num_records, p=[0.90, 0.10])
    
    multiple_lines = []
    for ps in phone_service:
        if ps == "No":
            multiple_lines.append("No phone service")
        else:
            multiple_lines.append(np.random.choice(["Yes", "No"], p=[0.45, 0.55]))
            
    internet_service = np.random.choice(["DSL", "Fiber optic", "No"], size=num_records, p=[0.44, 0.44, 0.12])
    
    online_security = []
    tech_support = []
    for iser in internet_service:
        if iser == "No":
            online_security.append("No internet service")
            tech_support.append("No internet service")
        else:
            online_security.append(np.random.choice(["Yes", "No"], p=[0.35, 0.65]))
            tech_support.append(np.random.choice(["Yes", "No"], p=[0.36, 0.64]))
            
    contract = np.random.choice(["Month-to-month", "One year", "Two year"], size=num_records, p=[0.55, 0.21, 0.24])
    paperless_billing = np.random.choice(["Yes", "No"], size=num_records, p=[0.59, 0.41])
    payment_method = np.random.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
        size=num_records,
        p=[0.34, 0.23, 0.22, 0.21]
    ).astype(object)
    
    # 4. Financial features
    # Base monthly charges depending on internet service type
    monthly_charges = []
    for iser in internet_service:
        if iser == "No":
            monthly_charges.append(np.round(np.random.uniform(18.0, 25.0), 2))
        elif iser == "DSL":
            monthly_charges.append(np.round(np.random.uniform(45.0, 85.0), 2))
        else: # Fiber optic
            monthly_charges.append(np.round(np.random.uniform(70.0, 118.0), 2))
    monthly_charges = np.array(monthly_charges, dtype=float)
    
    # Total charges roughly = tenure * monthly_charges + noise
    total_charges = tenure_months * monthly_charges + np.random.normal(0, 50, size=num_records)
    total_charges = np.round(np.maximum(total_charges, monthly_charges), 2)
    
    # Format total_charges as string to simulate dirty raw data with string spaces ' '
    total_charges_str = [str(val) for val in total_charges]
    
    # 5. Target Variable: Churn (Influenced by contract, tenure, internet service)
    churn_prob = []
    for i in range(num_records):
        prob = 0.25
        if contract[i] == "Month-to-month":
            prob += 0.25
        elif contract[i] == "Two year":
            prob -= 0.18
        if internet_service[i] == "Fiber optic":
            prob += 0.12
        if tenure_months[i] < 12:
            prob += 0.15
        elif tenure_months[i] > 48:
            prob -= 0.15
        prob = np.clip(prob, 0.05, 0.90)
        churn_prob.append(prob)
        
    churn = [("Yes" if np.random.rand() < p else "No") for p in churn_prob]
    
    # 6. Add non-informative / redundant feature for feature selection demonstration
    redundant_noise_feature = np.random.normal(50, 15, size=num_records)
    system_log_code = np.random.choice(["SYS_A", "SYS_B", "SYS_C"], size=num_records)
    
    # Build DataFrame
    df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Gender": genders_noisy,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "TenureMonths": tenure_months,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges_str,
        "SystemLogCode": system_log_code,
        "RandomNoiseScore": redundant_noise_feature,
        "Churn": churn
    })
    
    # --- Inject Real-World Flaws ---
    
    # A. Inject Missing Values (NaNs and blank spaces)
    missing_indices_g = np.random.choice(num_records, size=24, replace=False)
    df.loc[missing_indices_g, "Gender"] = np.nan
    
    missing_indices_s = np.random.choice(num_records, size=15, replace=False)
    df.loc[missing_indices_s, "SeniorCitizen"] = np.nan
    
    missing_indices_t = np.random.choice(num_records, size=18, replace=False)
    df.loc[missing_indices_t, "TenureMonths"] = np.nan
    
    missing_indices_mc = np.random.choice(num_records, size=20, replace=False)
    df.loc[missing_indices_mc, "MonthlyCharges"] = np.nan
    
    # Blank strings in TotalCharges (common issue in Telco datasets for new customers)
    blank_indices_tc = np.random.choice(num_records, size=25, replace=False)
    for idx in blank_indices_tc:
        df.loc[idx, "TotalCharges"] = " "
        
    missing_indices_pm = np.random.choice(num_records, size=16, replace=False)
    df.loc[missing_indices_pm, "PaymentMethod"] = np.nan

    # B. Inject Outliers in Numerical Features
    # MonthlyCharges extreme outliers (erroneous entry like 9999.0 or negative -150.0)
    df.loc[12, "MonthlyCharges"] = 9999.0
    df.loc[45, "MonthlyCharges"] = -150.0
    df.loc[88, "MonthlyCharges"] = 4500.0
    
    # TenureMonths extreme outliers
    df.loc[102, "TenureMonths"] = 350.0 # Unrealistic tenure in months (>30 yrs)
    df.loc[205, "TenureMonths"] = -12.0 # Negative tenure
    
    # C. Inject Duplicate Rows
    duplicate_rows = df.iloc[[10, 25, 50, 75, 100, 150, 200, 250, 300, 350]].copy()
    df = pd.concat([df, duplicate_rows], axis=0, ignore_index=True)
    
    # Shuffle dataframe
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    # Ensure directory exists and save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Raw dataset successfully created at '{output_path}' with shape {df.shape}.")
    return df

if __name__ == "__main__":
    generate_raw_churn_dataset()
