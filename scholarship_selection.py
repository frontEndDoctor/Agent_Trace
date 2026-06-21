import pandas as pd
import json
from datetime import datetime


def load_applications(path="applications.csv"):
    df = pd.read_csv(path)
    required = {"score", "nationality"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df


def log_demographics(df, selected):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "SCHOLARSHIP_SELECTION",
        "total_applicants": len(df),
        "total_selected": len(selected),
        "nationality_breakdown_all": (
            df["nationality"].value_counts().to_dict()
        ),
        "nationality_breakdown_selected": (
            selected["nationality"].value_counts().to_dict()
        ),
    }
    import os
    os.makedirs("audit-trail", exist_ok=True)
    with open("audit-trail/scholarship_audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

    print("\n--- Demographic Breakdown (Selected Candidates) ---")
    print(selected["nationality"].value_counts().to_string())


def main():
    df = load_applications()
    n_slots = max(1, min(int(len(df) * 0.1), 10))
    print(f"Selecting top {n_slots} candidates by score\n")

    df_sorted = df.sort_values("score", ascending=False)
    selected = df_sorted.head(n_slots)

    print("Selected candidates:")
    print(selected[["score", "nationality"]].to_string(index=False))

    log_demographics(df, selected)


if __name__ == "__main__":
    main()
