import json
import hashlib
import os
from datetime import datetime
import sys

LOG_FILE = "audit-trail/decisions.jsonl"
import json
import hashlib
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Audit Specialist")

@mcp.tool()
def append_to_audit_log(risk_flagged: str, developer_choice: str, rationale: str) -> str:
    """
    Appends a cryptographic hash-chained decision to the decisions.jsonl ledger.
    The Supervisor MUST call this tool after the developer makes a HITL choice.
    """
    log_file = "decisions.jsonl"
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
def get_previous_hash():
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        return "0000000000000000000000000000000000000000000000000000000000000000"
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()
        if lines:
            return json.loads(lines[-1]).get("hash", "")
    return "0000000000000000000000000000000000000000000000000000000000000000"

def log_decision(risk_category, developer_choice, rationale="None provided", supersedes_hash=None):
    previous_hash = get_previous_hash()
    
    # v2 Payload includes rationale and the correction flag
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "flagged_risk": risk_category,
        "developer_choice": developer_choice,
        "rationale": rationale,
        "supersedes_hash": supersedes_hash, # If this has a value, it corrects a past mistake
        "previous_hash": previous_hash
    }
    
    data_string = json.dumps(data, sort_keys=True)
    current_hash = hashlib.sha256(data_string.encode()).hexdigest()
    data["hash"] = current_hash
    
    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(data) + "\n")
        
    print(f"Decision logged. Hash: {current_hash[:8]}...")

if __name__ == "__main__":
    # Updated to handle optional arguments
    risk = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    choice = sys.argv[2] if len(sys.argv) > 2 else "Unknown"
    rationale = sys.argv[3] if len(sys.argv) > 3 else "None provided"
    supersedes = sys.argv[4] if len(sys.argv) > 4 else None
    
    log_decision(risk, choice, rationale, supersedes)