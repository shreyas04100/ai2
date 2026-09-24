# Technical Report: Customer Churn Data Preprocessing & Exploratory Data Analysis

**Assignment:** Python for Machine Learning & Data Preprocessing  
**Project Title:** Customer Churn Data Preprocessing & Exploratory Data Analysis  
**Domain:** Customer Analytics / Telecommunications  
**Output Files:** `data/processed/customer_churn_processed.csv`, `notebooks/churn_preprocessing_eda.ipynb`  

---

## 1. Project Background & Objective

In modern Machine Learning engineering, data preprocessing and Exploratory Data Analysis (EDA) consume 70–80% of project development time. Raw data collected from operational billing engines, web logs, and CRM databases is almost always corrupt, incomplete, un-scaled, or un-encoded. Machine Learning models—especially parametric models like Logistic Regression, Neural Networks, and distance-based algorithms like KNN—are highly sensitive to outliers, un-scaled numeric ranges, missing values, and high-cardinality noise.

The objective of this assignment is to demonstrate a rigorous, reproducible, step-by-step data preprocessing and EDA workflow in Python using **NumPy**, **Pandas**, **Matplotlib**, **Seaborn**, and **scikit-learn**.

---

## 2. Dataset Overview & Initial Inspection

The raw dataset (`data/raw/customer_churn_raw.csv`) consists of **1,210 customer records** across **19 feature attributes**.

### 2.1 Raw Data Schema
| Column Name | Data Type (Raw) | Description |
| :--- | :--- | :--- |
| `CustomerID` | `object` | Unique alphanumeric customer key (e.g. `CUST-10042`) |
| `Gender` | `object` | Customer gender (contains typos: `'female'`, `'F'`, `'Female'`, `'M'`, `'Male'`) |
| `SeniorCitizen` | `float64` | Binary indicator for senior citizen status (0.0 / 1.0) |
| `Partner` | `object` | Marital status indicator (`'Yes'` / `'No'`) |
| `Dependents` | `object` | Family dependents indicator (`'Yes'` / `'No'`) |
| `TenureMonths` | `float64` | Months as customer (contains negative & extreme outliers) |
| `PhoneService` | `object` | Voice subscription (`'Yes'` / `'No'`) |
| `MultipleLines` | `object` | Multiple line subscription (`'Yes'`, `'No'`, `'No phone service'`) |
| `InternetService` | `object` | Broadband service (`'DSL'`, `'Fiber optic'`, `'No'`) |
| `OnlineSecurity` | `object` | Security add-on (`'Yes'`, `'No'`, `'No internet service'`) |
| `TechSupport` | `object` | Technical support add-on (`'Yes'`, `'No'`, `'No internet service'`) |
| `Contract` | `object` | Subscription contract length (`'Month-to-month'`, `'One year'`, `'Two year'`) |
| `PaperlessBilling` | `object` | E-billing preference (`'Yes'` / `'No'`) |
| `PaymentMethod` | `object` | Payment option (`'Electronic check'`, `'Mailed check'`, `'Bank transfer'`, `'Credit card'`) |
| `MonthlyCharges` | `float64` | Recurring monthly bill in USD (contains extreme errors e.g. `$9999.0`) |
| `TotalCharges` | `object` | Cumulative historical charges in USD (dirty string with blank spaces `' '`) |
| `SystemLogCode` | `object` | Internal CRM log code (non-predictive system metadata) |
| `RandomNoiseScore` | `float64` | Synthetic Gaussian noise variable |
| `Churn` | `object` | Target outcome label (`'Yes'` / `'No'`) |

---

## 3. Detailed Step-by-Step Data Preprocessing Pipeline

### Step 3.1: Data Parsing & Formatting Cleaning
- **Problem**: `TotalCharges` was loaded as an `object` string dtype because 25 blank spaces (`" "`) were inserted during record creation for new customers with zero tenure. Additionally, negative values were present in `MonthlyCharges` and `TenureMonths`.
- **Action Taken**:
  1. Stripped whitespace and replaced blank strings (`""`) with `np.nan`.
  2. Coerced `TotalCharges` to `float64` numeric type.
  3. Replaced invalid negative values in `MonthlyCharges` and `TenureMonths` with `np.nan`.
  4. Standardized text formatting in `Gender` using string mapping (`'female'`, `'F'` $\rightarrow$ `'Female'`).
- **WHY**: Machine learning math cannot parse object string representations or handle non-physical negative billing amounts.

### Step 3.2: Duplicate Detection & Removal
- **Problem**: 10 duplicate customer rows were identified based on `CustomerID`.
- **Action Taken**: Dropped duplicate rows using `df.drop_duplicates(subset=['CustomerID'], keep='first')`.
- **Statistics**:
  - Raw dataset shape: `(1210, 19)`
  - Cleaned dataset shape: `(1200, 19)`
- **WHY**: Duplicates distort sample distributions, lead to data leakage during cross-validation, and over-emphasize repeated instances.

### Step 3.3: Missing Value Imputation
- **Problem**: Missing values were present in both continuous numerical columns and categorical columns (93 explicit NaNs + 25 blank string spaces = 118 missing cells total).
- **Imputation Strategy**:
  - **Numerical Columns** (`TenureMonths`, `MonthlyCharges`, `TotalCharges`, `SeniorCitizen`): **Median Imputation**.
    - *Rationale*: Numerical financial variables exhibit skewed distributions. Mean imputation is sensitive to extreme outliers, whereas median provides a robust central estimate.
  - **Categorical Columns** (`Gender`, `PaymentMethod`): **Mode Imputation**.
    - *Rationale*: Categorical variables have discrete modes; mode imputation preserves class probability mass.
- **Summary of Imputed Missing Values**:
  - `Gender`: 24 NaNs imputed with Mode (`'Female'`)
  - `SeniorCitizen`: 15 NaNs imputed with Median (`0.0`)
  - `TenureMonths`: 18 NaNs imputed with Median (`37.0`)
  - `MonthlyCharges`: 20 NaNs imputed with Median (`$70.62`)
  - `TotalCharges`: 25 NaNs/blanks imputed with Median (`$2445.85`)
  - `PaymentMethod`: 16 NaNs imputed with Mode (`'Electronic check'`)
  - **Resulting Missing Cells**: 0 across all columns.

### Step 3.4: Outlier Detection & Treatment (IQR-Based Capping)
- **Problem**: `MonthlyCharges` contained extreme entry errors (`$9999.0`, `-$150.0`), and `TenureMonths` contained unrealistic values (`350` months).
- **Action Taken**: Calculated lower and upper bounds using **IQR-based capping**:
  $$\text{IQR} = Q_3 - Q_1$$
  $$\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}$$
  $$\text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$$
  Values outside these boundaries were capped using `np.clip()`.
- **Outlier Capping Metrics**:
  - `MonthlyCharges`: 3 extreme outliers capped to range `[-14.50, 151.74]`
  - `TenureMonths`: 2 extreme outliers capped to range `[-55.50, 128.50]`
- **WHY Capping over Dropping**: IQR-based capping preserves valuable records and sample size while eliminating gradient destabilization in machine learning algorithms.

### Step 3.5: Feature Selection
- **Problem**: Including non-informative or high-cardinality key columns degrades model generalization and causes overfitting.
- **Action Taken**: Dropped 3 features:
  1. `CustomerID`: Unique string key with high cardinality and zero predictive value.
  2. `SystemLogCode`: Internal CRM metadata uncorrelated with churn behavior.
  3. `RandomNoiseScore`: Uncorrelated synthetic noise variable.
- **WHY**: Removing uninformative features reduces model dimensionality, speeds up training time, and mitigates the curse of dimensionality.

### Step 3.6: Categorical Variable Encoding
- **Problem**: Machine learning models require numeric tensor representations.
- **Action Taken**:
  1. **Binary Encoding (0/1)**: Applied to target `Churn` (`'No'`: 0, `'Yes'`: 1) and binary attributes (`Gender`, `SeniorCitizen`, `Partner`, `Dependents`, `PhoneService`, `PaperlessBilling`).
  2. **One-Hot Encoding (`pd.get_dummies`)**: Applied to multi-category nominal features (`Contract`, `InternetService`, `PaymentMethod`, `MultipleLines`, `OnlineSecurity`, `TechSupport`). We set `drop_first=True` to eliminate dummy variable multicollinearity.
- **Resulting Dimensions**: Expanded feature space to **23 numerical columns**.

### Step 3.7: Numerical Feature Scaling / Normalization
- **Problem**: Continuous numerical features (`TotalCharges`, `MonthlyCharges`, `TenureMonths`) operate on vastly different magnitude scales, whereas binary/one-hot features exist strictly as {0, 1} indicators.
- **Action Taken**: Applied `scikit-learn`'s `StandardScaler` (Z-score normalization) **exclusively to the 3 continuous numerical features** (`TenureMonths`, `MonthlyCharges`, and `TotalCharges`) to scale them to mean $\mu = 0$ and standard deviation $\sigma = 1$:
  $$z = \frac{x - \mu}{\sigma}$$
  *Note: Binary and one-hot encoded features are explicitly kept in their discrete {0, 1} encoding so that categorical indicator properties are preserved.*
- **WHY**: Ensures all continuous features contribute equally to optimization objective functions without skewing discrete indicator features.

---

## 4. Exploratory Data Analysis (EDA) & Key Findings

### 4.1 Target Variable Class Distribution
- **Total Samples**: 1,200 customers
- **Non-Churned (`No`)**: 876 customers (73.0%)
- **Churned (`Yes`)**: 324 customers (27.0%)
- **Insight**: Moderate class imbalance exists (~27% churn rate), typical for subscription-based telecommunications services.

### 4.2 Key Driver Analysis & Feature Correlations
1. **Contract Type**: Customers on **Month-to-month contracts** display a churn rate exceeding **42%**, compared to **<5%** for customers committed to Two-Year contracts.
2. **Internet Service**: **Fiber Optic** subscribers exhibit a higher churn rate (~38%) than DSL subscribers (~19%), likely due to higher price sensitivity or competitive promotion switching.
3. **Tenure & Total Charges**: Strong negative correlation ($r \approx -0.35$) between customer tenure and churn—newer customers (< 12 months) are at the highest risk of departing.

---

## 5. Quantitative Before-vs-After Comparison

| Quality Metric | Raw Dataset (`data/raw`) | Processed Dataset (`data/processed`) | Impact / Improvement |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 1,210 | 1,200 | 10 duplicate records removed |
| **Total Features** | 19 | 23 | Non-predictive dropped, nominal encoded |
| **Duplicate Rows** | 10 | 0 | 100% duplicate free |
| **Missing Cells (Total)** | 118 | 0 | 100% imputed via median/mode strategies |
| **Categorical Dtypes** | 14 (`object`) | 0 (`object`) | 100% converted to numerical numeric tensors |
| **Unscaled Continuous Variables** | 3 | 0 | Standardized to $\mu=0, \sigma=1$ |
| **Memory Usage (Deep)** | 1,144.57 KB | 215.75 KB | Memory footprint optimized for numeric arrays |

---

## 6. Project Structure & Output Artifacts

```
c:/Users/shrey/OneDrive/Desktop/Ai2/
├── data/
│   ├── raw/
│   │   └── customer_churn_raw.csv           # Raw dataset with intentional real-world flaws
│   └── processed/
│       └── customer_churn_processed.csv     # Fully cleaned, encoded, and scaled CSV
├── notebooks/
│   └── churn_preprocessing_eda.ipynb        # Fully executed Jupyter Notebook with outputs
├── src/
│   ├── __init__.py                          # Package initialization
│   ├── generate_dataset.py                  # Synthetic dataset generator script
│   ├── data_preprocessing.py                # Preprocessing pipeline OOP module
│   ├── eda.py                               # Exploratory data analysis & visualization script
│   └── utils.py                             # Statistical metrics and comparison helpers
├── outputs/
│   └── figures/
│       ├── churn_distribution.png           # Target distribution bar and pie chart
│       ├── churn_by_contract.png            # Churn rate breakdown by contract type
│       ├── churn_by_internetservice.png     # Churn breakdown by internet service
│       ├── outliers_before_after.png        # Outlier comparison boxplots
│       ├── correlation_matrix.png           # Pearson correlation heatmap
│       └── feature_scaling_comparison.png   # Unscaled vs Z-score scaled distribution
├── requirements.txt                         # Python dependencies specification
├── README.md                                # Project documentation & execution guide
└── report.md                                # Comprehensive technical report
```

---

## 7. Verification & Reproducibility Statement

All Python code scripts (`src/data_preprocessing.py`, `src/eda.py`) and the Jupyter Notebook (`notebooks/churn_preprocessing_eda.ipynb`) have been executed end-to-end without errors. Output metrics, preprocessed CSV files, and visualization charts are verified against the actual underlying dataset.
