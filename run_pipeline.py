import os
import pandas as pd
import numpy as np


def iqr_winsorize(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Apply IQR-based winsorisation to a numeric pandas Series.

    Values outside [Q1 - k*IQR, Q3 + k*IQR] are clipped to the bounds.

    Parameters
    ----------
    series : pd.Series
        Numeric series to winsorise.
    k : float, optional
        IQR multiplier (default is 1.5).

    Returns
    -------
    pd.Series
        Winsorised series.
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return series.clip(lower, upper)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the full cleaning pipeline to the dataset.

    Steps:
    1. Remove rows with impossible business values (e.g. negative rent)
    2. Treat outliers on selected columns via IQR-based winsorisation
    3. Impute missing values on selected columns using the median

    Parameters
    ----------
    df : pd.DataFrame
        Raw input dataframe.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.
    """
    df = df.copy()

    # 1. Remove impossible values (business rule)
    if "loyer_mensuel" in df.columns:
        mask_impossible = df["loyer_mensuel"] < 0
        nb_impossible = mask_impossible.sum()
        if nb_impossible > 0:
            print(f"[INFO] Removing {nb_impossible} rows with negative rent (loyer_mensuel < 0).")
        df = df[(df["loyer_mensuel"].isna()) | (df["loyer_mensuel"] >= 0)]

    # 2. IQR-based winsorisation for selected columns
    cols_with_outliers = ["taille", "poids", "revenu_estime_mois", "montant_pret"]
    for col in cols_with_outliers:
        if col in df.columns:
            df[col] = iqr_winsorize(df[col], k=1.5)
            print(f"[INFO] Applied IQR winsorisation on '{col}'.")
        else:
            print(f"[WARN] Column '{col}' not found in dataset; skipping winsorisation.")

    # 3. Median imputation for selected columns
    cols_to_impute = ["historique_credits", "score_credit", "loyer_mensuel"]
    for col in cols_to_impute:
        if col in df.columns:
            nb_nan_before = df[col].isna().sum()
            if nb_nan_before > 0:
                median_value = df[col].median()
                df[col] = df[col].fillna(median_value)
                nb_nan_after = df[col].isna().sum()
                print(
                    f"[INFO] Imputed {nb_nan_before} missing values in '{col}' "
                    f"with median = {median_value:.2f}. "
                    f"Remaining NaN: {nb_nan_after}."
                )
        else:
            print(f"[WARN] Column '{col}' not found in dataset; skipping imputation.")

    return df


def main():
    # Define project structure relative to this script
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_raw_dir = os.path.join(project_root, "data", "raw")
    data_processed_dir = os.path.join(project_root, "data", "processed")
    reports_dir = os.path.join(project_root, "reports")

    os.makedirs(data_raw_dir, exist_ok=True)
    os.makedirs(data_processed_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    raw_filename = "fichier-de-donnees-numeriques.csv"
    raw_path = os.path.join(data_raw_dir, raw_filename)

    if not os.path.exists(raw_path):
        raise FileNotFoundError(
            f"Raw data file not found at '{raw_path}'. "
            f"Please make sure '{raw_filename}' is placed in 'data/raw/'."
        )

    print(f"[INFO] Loading raw dataset from: {raw_path}")
    df_raw = pd.read_csv(raw_path)

    print(f"[INFO] Raw dataset shape: {df_raw.shape}")

    # Compute stats before cleaning
    stats_before = df_raw.describe().T
    stats_before["missing_pct"] = df_raw.isna().mean() * 100

    # Apply cleaning pipeline
    df_clean = clean_dataset(df_raw)

    print(f"[INFO] Cleaned dataset shape: {df_clean.shape}")

    # Compute stats after cleaning
    stats_after = df_clean.describe().T
    stats_after["missing_pct"] = df_clean.isna().mean() * 100

    # Export cleaned dataset
    clean_filename = "fichier-de-donnees-numeriques-clean.csv"
    clean_path = os.path.join(data_processed_dir, clean_filename)
    df_clean.to_csv(clean_path, index=False)
    print(f"[INFO] Cleaned dataset saved to: {clean_path}")

    # Export stats before & after
    stats_before_path = os.path.join(reports_dir, "stats_avant_nettoyage.csv")
    stats_after_path = os.path.join(reports_dir, "stats_apres_nettoyage.csv")

    stats_before.to_csv(stats_before_path)
    stats_after.to_csv(stats_after_path)

    print(f"[INFO] Stats BEFORE cleaning saved to: {stats_before_path}")
    print(f"[INFO] Stats AFTER cleaning saved to: {stats_after_path}")
    print("[INFO] Pipeline completed successfully.")


if __name__ == "__main__":
    main()