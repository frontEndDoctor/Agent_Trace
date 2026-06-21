from mcp.server.fastmcp import FastMCP
import json
import pandas as pd
from fairlearn.metrics import demographic_parity_difference, equalized_odds_difference
from sklearn.metrics import precision_score

# Initialize the FastMCP server
mcp = FastMCP("Fairness Agent")

@mcp.tool()
def evaluate_fairness_tradeoffs(prompt_context: str, target_variable: str) -> str:
    """
    Evaluates an ML model prompt against the three mutually incompatible 
    mathematical definitions of fairness demanded by the SpainGov Challenge framework.
    """
    # Simulate mathematical trade-offs for the requested target (e.g., recidivism, credit scoring)
    fairness_analysis = {
        "predictive_parity": {
            "proponent": "Northpointe / Risk Assessment Standard",
            "optimizes": "Equal Precision / Positive Predictive Value (PPV) across all demographic groups.",
            "consequence": "If base rates differ between groups, achieving this WILL violate Equalized Odds and Demographic Parity."
        },
        "equalized_odds": {
            "proponent": "ProPublica / Error-Rate Balance",
            "optimizes": "Equal False Positive Rates (FPR) and False Negative Rates (FNR) across groups.",
            "consequence": "Ensures no group is mistakenly misclassified at a higher rate, but harms overall predictive parity if base rates differ."
        },
        "demographic_parity": {
            "proponent": "Algorithmic Justice / Equality of Outcome",
            "optimizes": "Equal selection rates across groups regardless of historical base rates.",
            "consequence": "Achieves parity in real-world impact, but forces the model to ignore statistical predictive accuracy, causing an optimization tension."
        }
    }

    return json.dumps({
        "status": "FORK_DETECTED",
        "evaluation_type": "Mathematical Impossibility Theorem Analysis",
        "target_variable": target_variable,
        "regulatory_anchor": "EU AI Act Annex III / UN Declaration of Human Rights Art. 7",
        "tradeoffs": fairness_analysis,
        "guidance": (
            "The mathematical Impossibility Theorem proves you cannot satisfy all three criteria simultaneously. "
            "You must present Option A (Predictive Parity), Option B (Equalized Odds), or Option C (Demographic Parity) "
            "to the developer at the HITL gateway."
        )
    }, indent=2)
   


# using Fairlearn to calculate the actual mathematical trade-offs on a live dataset before the developer finalizes the model

@mcp.tool()
def calculate_live_fairness_metrics(y_true: list, y_pred: list, sensitive_features: list) -> str:
    """
    Uses Fairlearn to mathematically compute the Impossibility Theorem tradeoffs 
    on a live dataset before the developer finalizes the model.
    """
    # 1. Demographic Parity (Equality of Outcome)
    dp_diff = demographic_parity_difference(
        y_true, 
        y_pred, 
        sensitive_features=sensitive_features
    )
    
    # 2. Equalized Odds (ProPublica's Error-Rate Balance)
    eo_diff = equalized_odds_difference(
        y_true, 
        y_pred, 
        sensitive_features=sensitive_features
    )

    # 3. Predictive Parity (Northpointe's PPV/Precision balance)
    # Calculated manually per group to find the max difference in precision
    df = pd.DataFrame({'y_true': y_true, 'y_pred': y_pred, 'group': sensitive_features})
    precisions = df.groupby('group').apply(lambda x: precision_score(x['y_true'], x['y_pred'], zero_division=0))
    pp_diff = precisions.max() - precisions.min()

    report = {
        "status": "METRICS_CALCULATED",
        "live_tradeoffs": {
            "demographic_parity_gap": round(dp_diff, 4),
            "equalized_odds_gap": round(eo_diff, 4),
            "predictive_parity_gap": round(pp_diff, 4)
        },
        "hitl_action": "Route these exact mathematical gaps to the Supervisor to present to the developer."
    }

    return json.dumps(report, indent=2)

if __name__ == "__main__":
    mcp.run()