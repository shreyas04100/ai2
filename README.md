# Customer Churn Data Preprocessing & Exploratory Data Analysis

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)

A professional, beginner-friendly Python data science project demonstrating end-to-end **Data Preprocessing**, **Data Cleaning**, **Feature Engineering**, and **Exploratory Data Analysis (EDA)** on a Telecommunications Customer Churn dataset.

---

## 📌 Project Overview & Objectives

In machine learning workflows, raw real-world data is rarely ready for model training. Datasets commonly suffer from missing values, duplicate entries, inconsistent formatting, numerical outliers, and un-scaled features.

This repository satisfies the requirements for the internship assignment:
**"Python for Machine Learning & Data Preprocessing"**

### Key Learning & Implementation Objectives:
1. **Python & ML Fundamentals**: Modular scripting (`src/`), NumPy array operations, and Pandas DataFrame manipulation.
2. **Data Loading & Inspection**: Diagnostic exploration (`info()`, `describe()`, missing value counts, memory analysis).
3. **Data Cleaning & Deduplication**: Detecting string spaces, standardizing typo-laden categoricals, and removing duplicates.
4. **Missing Value Imputation**: Median strategy for numerical features, Mode strategy for categorical features.
5. **Outlier Detection & Capping**: Applying the 1.5x Interquartile Range (IQR) rule to cap extreme values.
6. **Feature Selection**: Identifying and dropping non-predictive IDs (`CustomerID`) and redundant noise variables.
7. **Categorical Variable Encoding**: Binary Label Encoding (0/1) and One-Hot Encoding (`drop_first=True`).
8. **Numerical Feature Scaling**: Z-score Standardization (`StandardScaler`) to normalize feature variance.
9. **Exploratory Data Analysis (EDA)**: Visualizing churn distributions, contract influences, and correlation heatmaps.
10. **Before-vs-After Comparison**: Quantitative verification of preprocessed dataset quality.

---

## 📁 Repository Structure

```
c:/Users/shrey/OneDrive/Desktop/Ai2/
├── data/
│   ├── raw/
│   │   └── customer_churn_raw.csv           # Synthetic raw dataset with intentional flaws
│   └── processed/
│       └── customer_churn_processed.csv     # Cleaned, encoded, and scaled CSV dataset
├── notebooks/
│   └── churn_preprocessing_eda.ipynb        # Fully executed Jupyter Notebook with outputs
├── src/
│   ├── __init__.py                          # Package initializer
│   ├── generate_dataset.py                  # Synthetic dataset generator script
│   ├── data_preprocessing.py                # Preprocessing pipeline script
│   ├── eda.py                               # Visualizations & EDA script
│   └── utils.py                             # Inspection and metrics helper module
├── outputs/
│   └── figures/
│       ├── churn_distribution.png           # Target class distribution chart
│       ├── churn_by_contract.png            # Churn distribution by contract type
│       ├── churn_by_internetservice.png     # Churn distribution by internet service
│       ├── outliers_before_after.png        # Outlier comparison boxplots
│       ├── correlation_matrix.png           # Feature correlation heatmap
│       └── feature_scaling_comparison.png   # Scaling distribution comparison
├── requirements.txt                         # Dependency requirements
├── report.md                                # Comprehensive technical report
└── README.md                                # Project guide & documentation
```

---

## 🚀 Quickstart & Reproducibility Guide

Follow these simple steps to replicate the entire project environment and pipeline on your local machine.

### Step 1: Clone or Open Project Workspace
Navigating to the project root directory:
```bash
cd c:/Users/shrey/OneDrive/Desktop/Ai2
```

### Step 2: Install Required Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### Step 3: Run Data Generation, Preprocessing & EDA Pipeline
Execute the modular Python scripts from the terminal:
```bash
# 1. Generate the raw synthetic dataset with realistic flaws
python src/generate_dataset.py

# 2. Run the complete data cleaning, imputation, encoding & scaling pipeline
python src/data_preprocessing.py

# 3. Generate all EDA figures and save them into outputs/figures/
python src/eda.py
```

### Step 4: Open and Run the Jupyter Notebook
Launch Jupyter Notebook to interactively step through the code, markdown explanations, and inline plots:
```bash
jupyter notebook notebooks/churn_preprocessing_eda.ipynb
```
Or execute the notebook head-to-tail via CLI:
```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/churn_preprocessing_eda.ipynb
```

---

## 📊 Preprocessing Before-vs-After Comparison

| Metric | Raw Dataset (`data/raw`) | Processed Dataset (`data/processed`) | Status |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 1,210 | 1,200 | 10 duplicates dropped |
| **Total Columns** | 19 | 23 | Non-predictive dropped, nominal encoded |
| **Duplicate Rows** | 10 | 0 | 100% duplicate free |
| **Missing Cells** | 118 | 0 | Fully imputed (Median/Mode) |
| **Data Types** | Mixed (`object`, `float64`) | 100% Numeric (`int32`, `float64`) | Model-ready |
| **Continuous Feature Scale** | Unscaled ($0 - \$9999) | Standardized ($\mu=0, \sigma=1$) | Normalized |
| **Memory Footprint** | 1,144.57 KB | 215.75 KB | Optimized numeric arrays |

---

## 💡 Key Business & Data Insights

1. **Contract Type Impact**: Customers on **Month-to-month contracts** exhibit a churn rate of **~42%**, compared to **<5%** for customers on Two-year contracts.
2. **Internet Service Impact**: Customers with **Fiber Optic** internet service churn at higher rates than DSL customers.
3. **Tenure Correlation**: Tenure has a negative correlation with churn ($r \approx -0.35$). Newer customers (<12 months) require targeted retention offers.

---

## 🛠️ Technology Stack
- **Language**: Python 3.11+
- **Data Manipulation**: Pandas, NumPy
- **Data Visualization**: Matplotlib, Seaborn
- **Machine Learning Preprocessing**: Scikit-Learn (`StandardScaler`, `MinMaxScaler`, `LabelEncoder`)
- **Notebook Environment**: Jupyter Notebook / NbConvert

---

## 📄 License & Attribution
This project was developed for the internship assignment **"Python for Machine Learning & Data Preprocessing"**.
