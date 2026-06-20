import json
import hashlib
import os
from datetime import datetime
import sys

LOG_FILE = "audit-trail/decisions.jsonl"

def get_previous_hash():
    """Reads the last line of the log to get the previous hash."""
    if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        return "0000000000000000000000000000000000000000000000000000000000000000"
    
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()
        if lines:
            last_entry = json.loads(lines[-1])
            return last_entry.get("hash", "")
    return "0000000000000000000000000000000000000000000000000000000000000000"

def log_decision(risk_category, developer_choice):
    previous_hash = get_previous_hash()
    timestamp = datetime.utcnow().isoformat()
    
    # Create the data payload
    data = {
        "timestamp": timestamp,
        "flagged_risk": risk_category,
        "developer_choice": developer_choice,
        "previous_hash": previous_hash
    }
    
    # Create a tamper-proof hash of this specific entry
    data_string = json.dumps(data, sort_keys=True)
    current_hash = hashlib.sha256(data_string.encode()).hexdigest()
    data["hash"] = current_hash
    
    # Append to the JSONL file
    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(data) + "\n")
        
    print(f"Decision securely logged with hash: {current_hash[:8]}...")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python audit_logger.py 'Risk Category' 'Developer Choice'")
    else:
        log_decision(sys.argv[1], sys.argv[2])