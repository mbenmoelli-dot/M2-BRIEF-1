# M2 BRIEF1 — Data Quality Pipeline for Numerical Dataset

## 🧠 Project context

FastIA wants to enrich its latest AI model with new numerical data.  
Before any model training, the raw data must go through a full **data quality pipeline**:

- exploratory analysis  
- audit of missing values  
- detection of anomalies and outliers  
- cleaning and transformation  
- documentation of every decision

This repository delivers a **reproducible and documented pipeline** to turn a noisy numerical dataset into a clean, consistent dataset ready for use in an AI project.

---

## 🎯 Objectives

- Inspect and understand the initial dataset (structure, distributions, issues)
- Detect and handle:
  - missing values
  - outliers
  - inconsistent / impossible values (e.g. negative rent)
- Apply a **reproducible cleaning pipeline**:
  - anomaly removal (business rules)
  - outlier treatment
  - missing value imputation
- Produce:
  - a **clean CSV file** ready for modelling
  - statistical reports **before vs after** cleaning
  - a **written summary report** explaining and justifying each choice

---

## 📂 Project structure

```text
M2 BRIEF1/
│
├── data/
│   ├── raw/                # Original noisy dataset (CSV)
│   └── processed/          # Clean dataset ready for AI
│
├── notebooks/
│   └── 01_exploration_nettoyage.ipynb  # Main analysis & cleaning notebook
│
├── reports/
│   ├── stats_avant_nettoyage.csv       # Descriptive stats before cleaning
│   ├── stats_apres_nettoyage.csv       # Descriptive stats after cleaning
│   └── rapport_synthese.md             # Human-readable summary report
│
├── run_pipeline.py         # Script to run the full cleaning pipeline
├── requirements.txt
└── README.md (this file)
```

---

## ⚙️ Installation & environment setup

### 1. Clone the repository

```bash
git clone <REPO_URL>
cd "C:\Users\benmo\source\repos\M2 BRIEF1"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On **Windows / PowerShell**:

```powershell
.\.venv\Scriptsctivate
```

You should see `(.venv)` at the beginning of your terminal prompt.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

Suggested `requirements.txt`:

```text
pandas
numpy
matplotlib
seaborn
missingno
scikit-learn
jupyter
```

(Additional libraries such as `plotly` or `altair` can be added if needed.)

---

## 🧪 Running the analysis (notebook)

1. Make sure the virtual environment is **activated**
2. Start Jupyter:

```bash
jupyter notebook
```

3. In your browser, open:
   - `notebooks/01_exploration_nettoyage.ipynb`

4. Run the notebook **cell by cell** to:
   - inspect the raw dataset
   - visualise missing values and outliers
   - apply cleaning steps
   - export the clean dataset and statistics

---

## 🏭 Running the pipeline as a script

For industrialisation, the same logic as in the notebook is implemented in **`run_pipeline.py`**.

From the project root:

```bash
python run_pipeline.py
```

This will:

- read the raw CSV from: `data/raw/fichier-de-donnees-numeriques.csv`
- apply the cleaning pipeline:
  - remove impossible values (e.g. negative rent)
  - treat outliers via IQR-based winsorisation
  - impute missing values (median-based strategy)
- export:
  - clean CSV → `data/processed/fichier-de-donnees-numeriques-clean.csv`
  - stats before cleaning → `reports/stats_avant_nettoyage.csv`
  - stats after cleaning → `reports/stats_apres_nettoyage.csv`

---

## 🧼 Cleaning methodology (overview)

### 1. Missing values & incomplete data

- Missing values are analysed **per column** and **per row**
- No column is dropped solely for having missing values
- Rows are *not* aggressively dropped: the goal is to **preserve as many records as possible**
- A strict rule is used instead: only **business-rule violations** (e.g. negative rent) are removed

### 2. Outliers

- Outliers are detected using the **IQR rule (Interquartile Range)**  
  - values below `Q1 - 1.5 * IQR` or above `Q3 + 1.5 * IQR` are considered extreme
- Instead of dropping rows, we use **winsorisation**:
  - extreme values are clipped to the lower/upper IQR bounds
  - this keeps the overall distribution shape while reducing the influence of outliers

### 3. Missing value imputation

- For key numeric features with missing values (e.g. credit history, credit score, rent):
  - the **median** is used as imputation strategy
  - this is robust to outliers and easy to interpret
- A more advanced method (`KNNImputer`) from scikit-learn can be plugged in if needed, but is optional

---

## 📊 Statistical analysis (before vs after)

The pipeline computes and saves descriptive statistics **before** and **after** cleaning:

- count, mean, standard deviation
- min, max, quartiles
- percentage of missing values

This allows you to:

- verify that the cleaning process did not distort the data
- check that missing values have been correctly handled
- validate that outliers are now under control

Outputs:

- `reports/stats_avant_nettoyage.csv`
- `reports/stats_apres_nettoyage.csv`

---

## 📁 Deliverables in this repository

As required in the brief, this repository contains:

- ✅ A **notebook or Python script** with the full, reproducible, well-commented pipeline  
  → `notebooks/01_exploration_nettoyage.ipynb` and `run_pipeline.py`
- ✅ A **clean CSV file** ready to be used in an AI project  
  → `data/processed/fichier-de-donnees-numeriques-clean.csv`
- ✅ A **summary report** describing:
  - the initial dataset
  - methodological choices (imputation, outliers, deletions)
  - a **before/after** comparison of key descriptive statistics  
  → `reports/rapport_synthese.md`

---

## 🏆 Performance & evaluation criteria

This project aims to satisfy the following criteria:

- **Clean, coherent final dataset**
  - no missing values
  - no impossible values (e.g. negative rent)
  - outliers treated in a controlled, explainable way

- **Reproducible and justified methodology**
  - environment setup documented
  - pipeline implemented both in a notebook and a script
  - every major decision explained in the summary report

- **Clear, professional documentation**
  - this README as an entry point
  - a structured summary report of the data cleaning
  - commented code for long-term maintainability

---

## 🤝 Author

This work is part of the **M2 — BRIEF1: Data quality and preprocessing for AI**.