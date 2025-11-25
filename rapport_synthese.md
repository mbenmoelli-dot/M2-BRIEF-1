# Synthesis report — Data quality pipeline for the numerical dataset

> Project: M2 BRIEF1 — FastIA  
> Goal: Clean and document a noisy numerical dataset before AI usage.

---

## 1. Initial dataset description

### 1.1. Source and context

The dataset was provided as a **numerical CSV file** and is intended to be used as an input for FastIA’s credit risk or financial scoring models.  
It contains multiple numerical features describing individuals and/or their financial situation (age, size, weight, estimated income, credit history, rent, loan amount, etc.).

The raw file is stored as:

- `data/raw/fichier-de-donnees-numeriques.csv`

### 1.2. Structure

At a high level, the dataset:

- has a relatively large number of rows (thousands of observations)
- contains only **numerical columns**
- includes typical financial / demographic variables such as:
  - age  
  - taille (height)  
  - poids (weight)  
  - revenu_estime_mois (estimated monthly income)  
  - historique_credits (credit history indicator)  
  - risque_personnel (personal risk score)  
  - score_credit (credit score)  
  - loyer_mensuel (monthly rent)  
  - montant_pret (loan amount)

### 1.3. Main issues identified

Exploratory analysis (EDA) highlighted the following problems:

- **Missing values** on several key variables
- **Outliers** on some financial variables (e.g. extremely high incomes or loan amounts)
- **Inconsistent business values**, for example:
  - negative rent values in `loyer_mensuel`
- Rows with up to several missing values, but no row with “almost all” features missing

These issues justify a structured cleaning process before any AI modelling.

---

## 2. Methodological choices

This section explains and justifies the main decisions taken in the cleaning pipeline.

### 2.1. Columns: keep or drop?

We computed the **percentage of missing values per column**.  
No column was found to be “quasi-empty” (e.g. > 90% missing).

**Decision:**

- ✅ **Keep all columns**
- ❌ Do not drop any feature based solely on missingness

**Rationale:**

- The variables are all potentially useful for the business use case
- Dropping columns would reduce the model’s expressiveness
- It is preferable to impute missing values with a transparent rule

---

### 2.2. Rows: deletion vs. imputation

We computed the **number of missing values per row**.  
Some rows had missing values in multiple columns, but very few were “completely broken”.

Instead of suppressing a fixed proportion of the dataset (e.g. 2% of rows), we applied a **business-driven rule**:

- ❌ **Rows with impossible values** (e.g. negative rent) are removed
- ✅ Rows with missing values on imputable features are **kept and imputed**

This approach:

- preserves as much data as possible
- avoids arbitrary deletion thresholds
- focuses on clear, justifiable rules (e.g. “rent cannot be negative”)

---

### 2.3. Outlier handling

Outliers were inspected visually using:

- histograms with density curves
- boxplots for each numerical feature

To mitigate the impact of extreme values without removing entire observations, we used:

- **IQR-based winsorisation**

**Method:**

For selected columns (e.g. `taille`, `poids`, `revenu_estime_mois`, `montant_pret`):

1. Compute Q1 (25th percentile) and Q3 (75th percentile)
2. Compute IQR = Q3 – Q1
3. Define lower and upper bounds:
   - lower = Q1 – 1.5 * IQR  
   - upper = Q3 + 1.5 * IQR
4. Clip values outside [lower, upper] to the corresponding bound

**Justification:**

- Keeps all rows
- Reduces variance caused by extreme values
- Preserves the overall distribution shape
- Method is standard, interpretable, and easy to reproduce

---

### 2.4. Missing value imputation

We focused on the main columns with missing values, for example:

- `historique_credits`
- `score_credit`
- `loyer_mensuel`

The imputation strategy chosen is:

- **median imputation** for each numerical feature

**Why the median?**

- robust to outliers
- simple, deterministic and easy to explain
- works well when we do not want to inject strong model assumptions into the data

An optional advanced method (`KNNImputer` from scikit-learn) can be activated in the code, but the default pipeline uses the median for clarity and stability.

---

## 3. Before/after comparison

To assess the impact of the cleaning steps, we computed descriptive statistics:

- **Before cleaning** → `reports/stats_avant_nettoyage.csv`
- **After cleaning** → `reports/stats_apres_nettoyage.csv`

For each feature, we can compare:

- count
- mean and standard deviation
- min, max
- quartiles
- percentage of missing values

### 3.1. Missing values

- Before cleaning:
  - several features had a non-negligible proportion of missing values
- After cleaning:
  - all selected features used in the model have **0% missing values**

### 3.2. Outliers and distributions

- Before:
  - some features presented very long tails or extreme values
  - some anomalies (e.g. negative rent)
- After:
  - outliers are reduced through winsorisation
  - impossible values are removed
  - overall distribution shape is preserved

The result is a dataset that is:

- more stable from a statistical point of view
- more consistent with business rules

---

## 4. Final dataset

The final cleaned dataset is exported as:

- `data/processed/fichier-de-donnees-numeriques-clean.csv`

It has the following properties:

- no missing values on key numerical features
- no impossible values (e.g. negative rent)
- reduced impact of extreme outliers
- stable and interpretable distributions

This file is now **ready to be used** as input for training or evaluating AI models.

---

## 5. Reproducibility and industrialisation

To ensure reproducibility, the cleaning steps are implemented in:

- a Jupyter notebook:  
  - `notebooks/01_exploration_nettoyage.ipynb`
- a standalone Python script:  
  - `run_pipeline.py`

Running the script from the project root:

```bash
python run_pipeline.py
```

will:

1. Load the raw dataset
2. Apply the same cleaning logic as in the notebook
3. Export:
   - the clean CSV file
   - statistics before and after cleaning

This allows the pipeline to be:

- integrated into larger workflows
- reused on future datasets with similar structure

---

## 6. Conclusion

The implemented data quality pipeline successfully:

- transforms a noisy, partially incomplete dataset  
  👉 into a clean, consistent, fully numerical dataset ready for AI
- handles missing values and outliers using transparent, well-known methods
- enforces basic business rules (e.g. no negative rent)
- documents every step for auditability and future maintenance

This approach can serve as a **template** for future datasets that FastIA will ingest in its AI models.