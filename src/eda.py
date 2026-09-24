"""
Exploratory Data Analysis (EDA) and Visualization Module.
Generates publication-quality charts and metrics saved into outputs/figures/.
"""

import os
import sys

# Ensure root project directory is in sys.path for direct script invocation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set global aesthetic theme
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

def generate_all_visualizations(raw_df: pd.DataFrame, processed_df: pd.DataFrame, output_dir: str = "outputs/figures") -> None:
    """
    Generates and saves all project charts for EDA and preprocessing report.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Target Variable (Churn) Distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    churn_counts = raw_df["Churn"].value_counts(dropna=False)
    
    colors = ["#2b5c8f", "#d9534f"]
    axes[0].bar(churn_counts.index.astype(str), churn_counts.values, color=colors, width=0.5, edgecolor="black")
    axes[0].set_title("Customer Churn Class Distribution (Counts)", fontweight="bold")
    axes[0].set_ylabel("Number of Customers")
    axes[0].set_xlabel("Churn Status")
    for i, v in enumerate(churn_counts.values):
        axes[0].text(i, v + 15, str(v), ha="center", fontweight="bold")
        
    axes[1].pie(churn_counts.values, labels=churn_counts.index.astype(str), autopct="%1.1f%%", colors=colors, startangle=140, explode=(0, 0.08), wedgeprops={"edgecolor": "black"})
    axes[1].set_title("Customer Churn Proportion (%)", fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "churn_distribution.png"), dpi=300)
    plt.close()
    print(f"[EDA] Saved target distribution plot to '{output_dir}/churn_distribution.png'")

    # 2. Churn Rate by Contract Type
    if "Contract" in raw_df.columns and "Churn" in raw_df.columns:
        plt.figure(figsize=(9, 5))
        contract_churn = raw_df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack() * 100
        contract_churn.plot(kind="bar", stacked=True, color=["#2b5c8f", "#d9534f"], figsize=(9, 5), edgecolor="black")
        plt.title("Churn Percentage by Contract Type", fontweight="bold")
        plt.xlabel("Contract Duration")
        plt.ylabel("Percentage (%)")
        plt.xticks(rotation=0)
        plt.legend(title="Churn Status", loc="upper right")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "churn_by_contract.png"), dpi=300)
        plt.close()
        print(f"[EDA] Saved churn by contract plot to '{output_dir}/churn_by_contract.png'")

    # 3. Churn Rate by Internet Service
    if "InternetService" in raw_df.columns and "Churn" in raw_df.columns:
        plt.figure(figsize=(9, 5))
        is_churn = raw_df.groupby("InternetService")["Churn"].value_counts(normalize=True).unstack() * 100
        is_churn.plot(kind="bar", color=["#2b5c8f", "#d9534f"], figsize=(9, 5), edgecolor="black")
        plt.title("Churn Distribution Across Internet Service Types", fontweight="bold")
        plt.xlabel("Internet Service Type")
        plt.ylabel("Percentage (%)")
        plt.xticks(rotation=0)
        plt.legend(title="Churn Status")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "churn_by_internetservice.png"), dpi=300)
        plt.close()
        print(f"[EDA] Saved churn by internet service plot to '{output_dir}/churn_by_internetservice.png'")

    # 4. Outliers Comparison (Before vs After Capping)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Raw MonthlyCharges with outliers
    raw_mc = pd.to_numeric(raw_df["MonthlyCharges"], errors="coerce").dropna()
    sns.boxplot(x=raw_mc, ax=axes[0, 0], color="#f0ad4e")
    axes[0, 0].set_title("Raw Monthly Charges (Before IQR Capping)", fontweight="bold")
    axes[0, 0].set_xlabel("Monthly Charges ($)")
    
    # Processed MonthlyCharges
    sns.boxplot(x=processed_df["MonthlyCharges"], ax=axes[0, 1], color="#5cb85c")
    axes[0, 1].set_title("Processed Monthly Charges (After Outlier Capping & Scaling)", fontweight="bold")
    axes[0, 1].set_xlabel("Standardized Monthly Charges")
    
    # Raw Tenure
    raw_tn = pd.to_numeric(raw_df["TenureMonths"], errors="coerce").dropna()
    sns.boxplot(x=raw_tn, ax=axes[1, 0], color="#f0ad4e")
    axes[1, 0].set_title("Raw Tenure Months (Before IQR Capping)", fontweight="bold")
    axes[1, 0].set_xlabel("Tenure (Months)")
    
    # Processed Tenure
    sns.boxplot(x=processed_df["TenureMonths"], ax=axes[1, 1], color="#5cb85c")
    axes[1, 1].set_title("Processed Tenure Months (After Outlier Capping & Scaling)", fontweight="bold")
    axes[1, 1].set_xlabel("Standardized Tenure Months")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "outliers_before_after.png"), dpi=300)
    plt.close()
    print(f"[EDA] Saved outlier comparison plot to '{output_dir}/outliers_before_after.png'")

    # 5. Correlation Heatmap of Processed Features
    plt.figure(figsize=(12, 9))
    corr_matrix = processed_df.corr()
    
    # Select top correlated features with Churn
    if "Churn" in corr_matrix.columns:
        churn_corr = corr_matrix["Churn"].sort_values(ascending=False)
        top_cols = churn_corr.index[:12] # Top 12 features
        sub_corr = corr_matrix.loc[top_cols, top_cols]
    else:
        sub_corr = corr_matrix.iloc[:12, :12]
        
    mask = np.triu(np.ones_like(sub_corr, dtype=bool))
    sns.heatmap(sub_corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
    plt.title("Correlation Heatmap of Processed Features with Churn", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_matrix.png"), dpi=300)
    plt.close()
    print(f"[EDA] Saved correlation matrix heatmap to '{output_dir}/correlation_matrix.png'")

    # 6. Feature Scaling Distribution Comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    sns.histplot(raw_mc[raw_mc < 500], kde=True, ax=axes[0], color="#2b5c8f", bins=30)
    axes[0].set_title("Raw Monthly Charges Distribution (Unscaled)", fontweight="bold")
    axes[0].set_xlabel("Monthly Charges ($)")
    
    sns.histplot(processed_df["MonthlyCharges"], kde=True, ax=axes[1], color="#27ae60", bins=30)
    axes[1].set_title("Standardized Monthly Charges Distribution (Z-Score)", fontweight="bold")
    axes[1].set_xlabel("Standardized Value (Mean=0, Std=1)")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "feature_scaling_comparison.png"), dpi=300)
    plt.close()
    print(f"[EDA] Saved feature scaling comparison plot to '{output_dir}/feature_scaling_comparison.png'")

if __name__ == "__main__":
    from src.data_preprocessing import ChurnDataPreprocessor
    preprocessor = ChurnDataPreprocessor()
    raw_df, processed_df = preprocessor.run_pipeline(
        raw_filepath="data/raw/customer_churn_raw.csv",
        output_filepath="data/processed/customer_churn_processed.csv"
    )
    generate_all_visualizations(raw_df, processed_df)
