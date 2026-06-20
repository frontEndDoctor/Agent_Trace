from mcp.server.fastmcp import FastMCP
import re
import json

# Initialize the FastMCP server. This name will appear in your logs.
mcp = FastMCP("Privacy Specialist")

@mcp.tool()
def scan_for_privacy_risks(code_snippet: str) -> str:
    """
    Scans a given code snippet or prompt for Personally Identifiable Information (PII)
    and protected demographic attributes (EU AI Act compliance).
    """
    risks = []
    
    # 1. Check for Protected Attributes (Bias / Fairness risk)
    protected_keywords = ["age", "gender", "race", "ethnicity", "religion", "sexual_orientation"]
    found_attributes = [kw for kw in protected_keywords if kw in code_snippet.lower()]
    
    if found_attributes:
        risks.append(f"Protected attributes detected: {', '.join(found_attributes)}")
        
    # 2. Check for PII (Data Privacy risk)
    # Basic regex for catching hardcoded email addresses
    if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", code_snippet):
        risks.append("Email addresses (PII) detected.")
        
    # Keyword check for high-risk data fields
    if "password" in code_snippet.lower() or "ssn" in code_snippet.lower():
        risks.append("Highly sensitive data fields (password/SSN) detected.")
        
    # 3. Format and return the payload to the Supervisor
    if risks:
        return json.dumps({
            "status": "RISK_FOUND", 
            "details": risks, 
            "mitigation": "Trigger Human-in-the-Loop Gateway. Present Option 1 (Anonymize Data) and Option 2 (Standard Execution)."
        }, indent=2)
        
    return json.dumps({
        "status": "SAFE", 
        "details": "No privacy risks detected."
    })

if __name__ == "__main__":
    # Start the server listening on standard input/output
    mcp.run()