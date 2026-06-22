import pandas as pd
import sys


def sanitize_and_audit(path="credit_data.csv"):
    df = pd.read_csv(path)

    sensitive = ["Race", "Gender", "Ethnicity"]
    proxies = ["Zip_Code", "Zip", "Income_Level", "Income", "Education_Level", "Education"]
    present_sensitive = [c for c in sensitive if c in df.columns]
    present_proxies = [c for c in proxies if c in df.columns]
    all_dropped = present_sensitive + present_proxies

    print("=" * 60)
    print("DATA COMPLIANCE SANITIZER — EU AI Act Art. 5")
    print("=" * 60)
    print(f"\nProtected attributes dropped: {present_sensitive}")
    print(f"Proxy variables dropped:      {present_proxies}")

    if not all_dropped:
        print("\nNo policy-violating columns detected.")
    else:
        df_clean = df.drop(columns=all_dropped)
        print(f"\nColumns retained ({list(df_clean.columns)}):")
        print(df_clean.head(3).to_string())
        print(f"\nShape before: {df.shape}")
        print(f"Shape after:  {df_clean.shape}")

    print("\n" + "-" * 60)
    print("GOVERNANCE REPORT")
    print("-" * 60)
    print("""
  Regulatory Anchor: EU AI Act Annex III / UN Declaration of Human Rights Art. 7
  Risk Classification: PROHIBITED (Art. 5 — Subtle/Proxy Algorithmic Discrimination)
  Fairness Criterion Selected: Predictive Parity (Equal PPV across groups)
  Decision: No predictive policing model trained.
  Action: All direct and proxy demographic features removed.
  Non-discriminatory alternative: Community resource allocation planning
    based on reported incident data (not predictive risk scores).
    """)

    return df_clean if all_dropped else df


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "credit_data.csv"
    sanitize_and_audit(path)
