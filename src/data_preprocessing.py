"""
Data Preprocessing Module for Customer Churn Dataset.
Implements modular, robust, and reproducible data cleaning, imputation, outlier handling,
encoding, feature scaling, and feature selection pipelines.
"""

import os
import sys
from typing import Tuple, Dict, List, Any

# Ensure root project directory is in sys.path for direct script invocation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

from src.utils import compute_iqr_outliers

class ChurnDataPreprocessor:
    """
    Stateful Data Preprocessor for Customer Churn Data.
    Maintains transformer states (scalers, encoders) for train/test data consistency.
    """
    
    def __init__(self, scaling_method: str = "standard"):
        self.scaling_method = scaling_method
        self.scaler = StandardScaler() if scaling_method == "standard" else MinMaxScaler()
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.onehot_columns: List[str] = []
        self.feature_names_out: List[str] = []
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Loads dataset from CSV file path."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found at path: {file_path}")
        return pd.read_csv(file_path)

    def clean_initial_formatting(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans initial string inconsistencies and converts blank spaces to NaNs.
        Specifically fixes dirty string total charges and invalid numerical signs.
        """
        df = df.copy()
        
        # 1. Replace empty whitespace strings with NaN in TotalCharges
        if "TotalCharges" in df.columns:
            df["TotalCharges"] = df["TotalCharges"].astype(str).str.strip()
            df["TotalCharges"] = df["TotalCharges"].replace("", np.nan)
            df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
            
        # 2. Fix negative numeric anomalies (e.g., negative monthly charges or negative tenure)
        if "MonthlyCharges" in df.columns:
            df.loc[df["MonthlyCharges"] < 0, "MonthlyCharges"] = np.nan
            
        if "TenureMonths" in df.columns:
            df.loc[df["TenureMonths"] < 0, "TenureMonths"] = np.nan
            
        return df

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detects and drops duplicate rows based on CustomerID or full row content."""
        df = df.copy()
        initial_count = len(df)
        
        # Primary check: duplicate CustomerID
        if "CustomerID" in df.columns:
            df = df.drop_duplicates(subset=["CustomerID"], keep="first")
        else:
            df = df.drop_duplicates(keep="first")
            
        removed_count = initial_count - len(df)
        print(f"[Data Cleaning] Removed {removed_count} duplicate records.")
        return df

    def standardize_categorical_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes inconsistent categorical text formatting (case typos, abbreviations).
        """
        df = df.copy()
        if "Gender" in df.columns:
            gender_map = {
                "female": "Female", "F": "Female", "Female": "Female",
                "male": "Male", "M": "Male", "Male": "Male"
            }
            df["Gender"] = df["Gender"].map(gender_map)
            
        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Imputes missing values using statistical strategies:
        - Numerical columns: Median imputation (robust against skewed values)
        - Categorical columns: Mode imputation (most frequent category)
        """
        df = df.copy()
        
        # Identify missing values before imputation
        num_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        
        # Impute Numerical
        for col in num_cols:
            if df[col].isna().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"[Imputation] Numerical column '{col}' missing values imputed with median ({median_val:.2f}).")
                
        # Impute Categorical
        for col in cat_cols:
            if col != "CustomerID" and df[col].isna().sum() > 0:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
                print(f"[Imputation] Categorical column '{col}' missing values imputed with mode ('{mode_val}').")
                
        return df

    def detect_and_cap_outliers(self, df: pd.DataFrame, num_cols: List[str] = None) -> pd.DataFrame:
        """
        Detects and caps outliers using the 1.5x IQR boundary rule to preserve data integrity
        without dropping valid records.
        """
        df = df.copy()
        if num_cols is None:
            num_cols = ["MonthlyCharges", "TenureMonths", "TotalCharges"]
            num_cols = [c for c in num_cols if c in df.columns]
            
        for col in num_cols:
            lower_b, upper_b, mask = compute_iqr_outliers(df[col])
            outlier_count = mask.sum()
            if outlier_count > 0:
                print(f"[Outlier Treatment] Column '{col}': Capping {outlier_count} outliers to range [{lower_b:.2f}, {upper_b:.2f}].")
                df[col] = np.clip(df[col], lower_b, upper_b)
                
        return df

    def perform_feature_selection(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Removes non-informative, redundant, or random features.
        - Primary key: CustomerID (has no predictive signal for machine learning)
        - System codes / noise: SystemLogCode, RandomNoiseScore
        """
        df = df.copy()
        drop_cols = ["CustomerID", "SystemLogCode", "RandomNoiseScore"]
        actual_dropped = [c for c in drop_cols if c in df.columns]
        
        df = df.drop(columns=actual_dropped)
        print(f"[Feature Selection] Dropped non-predictive/redundant columns: {actual_dropped}")
        return df, actual_dropped

    def encode_categorical_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encodes binary categorical features using Binary Label Encoding (0/1)
        and multi-category nominal features using One-Hot Encoding (pd.get_dummies).
        """
        df = df.copy()
        
        # 1. Encode Target Variable 'Churn'
        if "Churn" in df.columns:
            df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1}).astype(int)
            
        # 2. Binary Categorical Features (2 unique values) -> Binary Mapping (0/1)
        binary_cols = ["Gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService", "PaperlessBilling"]
        for col in binary_cols:
            if col in df.columns:
                if col == "Gender":
                    df[col] = df[col].map({"Female": 0, "Male": 1}).fillna(0).astype(int)
                else:
                    df[col] = df[col].map({"No": 0, "Yes": 1, 0: 0, 1: 1}).fillna(0).astype(int)
                    
        # 3. Nominal Multi-Category Features -> One-Hot Encoding
        multi_cat_cols = ["MultipleLines", "InternetService", "OnlineSecurity", "TechSupport", "Contract", "PaymentMethod"]
        multi_cat_cols = [c for c in multi_cat_cols if c in df.columns]
        
        if multi_cat_cols:
            df = pd.get_dummies(df, columns=multi_cat_cols, drop_first=True, dtype=int)
            
        print(f"[Categorical Encoding] Encoded categorical variables. Total columns after encoding: {df.shape[1]}")
        return df

    def scale_numerical_features(self, df: pd.DataFrame, num_cols: List[str] = None) -> pd.DataFrame:
        """
        Scales continuous numerical features using StandardScaler or MinMaxScaler.
        """
        df = df.copy()
        if num_cols is None:
            num_cols = ["TenureMonths", "MonthlyCharges", "TotalCharges"]
            num_cols = [c for c in num_cols if c in df.columns]
            
        if num_cols:
            scaled_array = self.scaler.fit_transform(df[num_cols])
            for i, col in enumerate(num_cols):
                df[col] = scaled_array[:, i]
            print(f"[Feature Scaling] Scaled numerical columns {num_cols} using {self.scaling_method.capitalize()}Scaler.")
            
        return df

    def run_pipeline(self, raw_filepath: str, output_filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Executes the end-to-end data cleaning, preprocessing, and encoding pipeline.
        Returns: (raw_df, processed_df)
        """
        print("=== STAGE 1: Data Loading ===")
        raw_df = self.load_data(raw_filepath)
        print(f"Loaded raw dataset with shape: {raw_df.shape}")
        
        df = raw_df.copy()
        
        print("\n=== STAGE 2: Formatting & Duplicate Removal ===")
        df = self.clean_initial_formatting(df)
        df = self.remove_duplicates(df)
        df = self.standardize_categorical_values(df)
        
        print("\n=== STAGE 3: Missing Value Imputation ===")
        df = self.handle_missing_values(df)
        
        print("\n=== STAGE 4: Outlier Detection & Treatment ===")
        df = self.detect_and_cap_outliers(df)
        
        print("\n=== STAGE 5: Feature Selection ===")
        df, dropped = self.perform_feature_selection(df)
        
        print("\n=== STAGE 6: Categorical Variable Encoding ===")
        df = self.encode_categorical_variables(df)
        
        print("\n=== STAGE 7: Feature Scaling ===")
        df = self.scale_numerical_features(df)
        
        # Save processed dataset
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        df.to_csv(output_filepath, index=False)
        print(f"\n[Success] Processed dataset saved to '{output_filepath}' with shape {df.shape}.")
        
        return raw_df, df

if __name__ == "__main__":
    preprocessor = ChurnDataPreprocessor(scaling_method="standard")
    raw_df, processed_df = preprocessor.run_pipeline(
        raw_filepath="data/raw/customer_churn_raw.csv",
        output_filepath="data/processed/customer_churn_processed.csv"
    )
