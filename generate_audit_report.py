import os
import json

def generate_report():
    # Force the script to look in its current exact directory (the project root)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(root_dir, "decisions.jsonl")
    report_file = os.path.join(root_dir, "Auditor_Report.md")

    # Check if the file actually exists before trying to read it
    if not os.path.exists(log_file):
        print(f"Error: Could not find the audit log at {log_file}")
        print("Fix: Go back to VS Code and tell the AI to 'log my decision' to create the file!")
        return

    # Read the JSONL file
    with open(log_file, "r") as f:
        lines = f.readlines()

    if not lines:
        print("The log file exists but is empty.")
        return

    # Generate the Markdown report
    with open(report_file, "w") as out:
        out.write("# 🛡️ UNDPK Cryptographic Audit Report\n\n")
        out.write("This document is automatically generated from the immutable `decisions.jsonl` ledger.\n\n")
        out.write("## Regulatory Compliance Ledger\n\n")
        out.write("| Timestamp | Governance Risk | Developer Choice | Rationale | Hash Chain |\n")
        out.write("|-----------|-----------------|------------------|-----------|------------|\n")
        
        for line in lines:
            try:
                entry = json.loads(line.strip())
                timestamp = entry.get("timestamp", "N/A")[:16] # Shorten timestamp for readability
                risk = entry.get("governance_risk", "N/A")
                choice = entry.get("developer_choice", "N/A")
                rationale = entry.get("rationale", "N/A")
                hash_val = entry.get("hash", "N/A")[:8] + "..." # Show only first 8 chars of hash
                
                out.write(f"| {timestamp} | {risk} | {choice} | {rationale} | `{hash_val}` |\n")
            except json.JSONDecodeError:
                continue
    
    print(f"✅ Success! Audit report generated at: {report_file}")

if __name__ == "__main__":
    generate_report()