#!/usr/bin/env python3
import json
import warnings
import sys
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, roc_auc_score,
    confusion_matrix
)

warnings.filterwarnings("ignore")

BIAS_DISCLAIMER = """
======================================================================
BIAS DISCLAIMER
This model was trained WITHOUT protected attributes (race, sex, age)
to reduce discriminatory risk. However, prior_arrests may still act as
a proxy for systemic biases in the criminal justice system.
Predictions should NOT be used as the sole basis for decisions
affecting individuals. Always pair with human review and ongoing
fairness monitoring.
======================================================================
"""


def load_data(path="compas.csv"):
    df = pd.read_csv(path)
    required = {"prior_arrests", "two_year_recid", "race", "sex"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(f"Missing columns: {missing}")
    return df


def evaluate_fairness(model, X_test, df_test):
    print("\n--- Fairness Evaluation (Predictive Parity) ---")
    results = []
    for group in ["race", "sex"]:
        for val in df_test[group].unique():
            mask = df_test[group] == val
            if mask.sum() < 10:
                continue
            X_group = X_test[mask]
            y_true = df_test.loc[mask, "two_year_recid"]
            if X_group.shape[0] == 0:
                continue
            y_pred = model.predict(X_group)
            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, zero_division=0)
            rec = recall_score(y_true, y_pred, zero_division=0)
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
            results.append({
                "group": group,
                "value": val,
                "count": int(mask.sum()),
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "fpr": round(fpr, 4),
            })
            print(f"  {group}={val:12s}  n={int(mask.sum()):4d}  "
                  f"acc={acc:.3f}  prec={prec:.3f}  rec={rec:.3f}  fpr={fpr:.3f}")
    return results


def log_audit(entry):
    with open("audit-trail/model_operations.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    print("Loading data...")
    df = load_data()

    features = ["prior_arrests"]
    target = "two_year_recid"

    X = df[features].values
    y = df[target].values
    groups = df[["race", "sex"]].copy()

    X_train, X_test, y_train, y_test, _, df_test_idx = train_test_split(
        X, y, groups, test_size=0.2, random_state=42
    )
    # Align df_test with the test indices
    df_test = df.iloc[df_test_idx.index]

    log_audit({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "TRAINING_START",
        "features_used": features,
        "features_excluded": ["race", "sex", "age"],
        "model": "RandomForestClassifier",
        "n_train": len(X_train),
        "n_test": len(X_test),
    })

    print(f"\nTraining RandomForest on features: {features}")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n--- Model Performance ---")
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  AUC-ROC:   {roc_auc_score(y_test, y_prob):.4f}")
    print(f"  Feature importance: {dict(zip(features, model.feature_importances_))}")

    fairness_results = evaluate_fairness(model, X_test, df_test)

    log_audit({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "TRAINING_COMPLETE",
        "features_used": features,
        "metrics": {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "auc_roc": float(roc_auc_score(y_test, y_prob)),
        },
        "fairness_evaluation": fairness_results,
    })

    print(BIAS_DISCLAIMER)


if __name__ == "__main__":
    main()
