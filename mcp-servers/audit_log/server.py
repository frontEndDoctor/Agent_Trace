import json
import hashlib
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Audit Log")

@mcp.tool()
def append_to_audit_log(risk_flagged: str, developer_choice: str, rationale: str) -> str:
    """
    Appends a cryptographic hash-chained decision to the decisions.jsonl ledger.
    """
    # 1. Force the script to find the absolute root of your project
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir)) # Goes up 2 levels
    log_file = os.path.join(root_dir, "decisions.jsonl")
    
    prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    
    # Read previous hash to maintain the cryptographic chain
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
            if lines:
                last_entry = json.loads(lines[-1].strip())
                prev_hash = last_entry.get("hash", prev_hash)

    # Create the new entry payload
    entry = {
        "timestamp": datetime.now().isoformat(),
        "governance_risk": risk_flagged,
        "developer_choice": developer_choice,
        "rationale": rationale,
        "previous_hash": prev_hash
    }
    
    # Calculate the SHA-256 hash of the current entry
    entry_string = json.dumps(entry, sort_keys=True)
    entry["hash"] = hashlib.sha256(entry_string.encode()).hexdigest()
    
    # Append to the immutable ledger
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
        
    return f"SUCCESS: Decision cryptographically logged. Hash: {entry['hash'][:8]}..."

if __name__ == "__main__":
    mcp.run()