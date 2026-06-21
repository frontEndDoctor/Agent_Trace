import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import json
from datetime import datetime
warnings.filterwarnings("ignore")


def demographic_parity(y_pred, group_mask):
    accept_rate_group = y_pred[group_mask].mean()
    accept_rate_total = y_pred.mean()
    return accept_rate_group / accept_rate_total if accept_rate_total > 0 else 1.0


def equalized_odds(y_true, y_pred, group_mask):
    tn, fp, fn, tp = confusion_matrix(y_true[group_mask], y_pred[group_mask]) labels[0,1].ravel()
    tpr_group = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr_group = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    tn_t, fp_t, fn_t, tp_t = confusion_matrix(y_true, y_pred) labels[0,1].ravel()
    tpr_total = tp_t / (tp_t + fn_t) if (tp_t + fn_t) > 0 else 0.0
    fpr_total = fp_t / (fp_t + tn_t) if (fp_t + tn_t) > 0 else 0.0

    return {
        "tpr_ratio": tpr_group / tpr_total if tpr_total > 0 else 1.0,
        "fpr_ratio": fpr_group / fpr_total if fpr_total > 0 else 1.0,
    }


def predictive_parity(y_true, y_pred, group_mask):
    ppv_group = y_true[group_mask][y_pred[group_mask] == 1].mean() if y_pred[group_mask].sum() > 0 else 0.0
    ppv_total = y_true[y_pred == 1].mean() if y_pred.sum() > 0 else 0.0
    return ppv_group / ppv_total if ppv_total > 0 else 1.0


def main():
    df = pd.read_csv("loan_predictions.csv")
    required = {"age_group", "y_true", "y_pred"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    print("=" * 60)
    print("LOAN APPROVAL MODEL — FAIRNESS EVALUATION")
    print("=" * 60)
    print(f"\nNote: It is mathematically impossible to satisfy demographic parity,")
    print(f"equalized odds, and predictive parity simultaneously unless base rates")
    print(f"are equal across groups or the model is perfect (Kleinberg et al.).")
    print(f"These metrics reveal trade-offs, not a pass/fail.\n")

    results = []
    for age_val in sorted(df["age_group"].unique()):
        mask = df["age_group"] == age_val
        y_true = df["y_true"].values
        y_pred = df["y_pred"].values

        dp = demographic_parity(y_pred, mask.values)
        eo = equalized_odds(y_true, y_pred, mask.values)
        pp = predictive_parity(y_true, y_pred, mask.values)

        results.append({
            "age_group": age_val,
            "count": int(mask.sum()),
            "demographic_parity": round(dp, 4),
            "equalized_odds_tpr_ratio": round(eo["tpr_ratio"], 4),
            "equalized_odds_fpr_ratio": round(eo["fpr_ratio"], 4),
            "predictive_parity": round(pp, 4),
        })

    print(f"{'Age Group':<12} {'n':<6} {'DP':<8} {'EO-TPR':<8} {'EO-FPR':<8} {'PP':<8}")
    print("-" * 50)
    for r in results:
        dp_s = f"{r['demographic_parity']:.2f}"
        eo_tpr_s = f"{r['equalized_odds_tpr_ratio']:.2f}"
        eo_fpr_s = f"{r['equalized_odds_fpr_ratio']:.2f}"
        pp_s = f"{r['predictive_parity']:.2f}"
        print(f"{r['age_group']:<12} {r['count']:<6} {dp_s:<8} {eo_tpr_s:<8} {eo_fpr_s:<8} {pp_s:<8}")

    print("\n--- Interpretation ---")
    print("All metrics should be close to 1.0 for perfect parity.")
    print("Values < 0.8 or > 1.2 suggest meaningful disparity for that group.")
# -----------------------------------------
    # UN TECH OVER: AUTOMATED AUDIT EXPORT
    # -----------------------------------------
    audit_filename = f"audit_log_fairness_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    audit_payload = {
        "timestamp": datetime.now().isoformat(),
        "evaluation_type": "Demographic Parity & Equalized Odds",
        "human_rights_framework": "UNESCO AI Ethics (Non-Discrimination)",
        "results": results
    }
    
    with open(audit_filename, "w") as f:
        json.dump(audit_payload, f, indent=4)
        
    print(f"\n[+] Governance Audit automatically saved to: {audit_filename}")

if __name__ == "__main__":
    import warnings
    main()
