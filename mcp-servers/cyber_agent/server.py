from mcp.server.fastmcp import FastMCP
import re
import json

# Initialize the FastMCP server
mcp = FastMCP("Cybersecurity Agent")

@mcp.tool()
def scan_for_vulnerabilities(code_snippet: str) -> str:
    """
    Scans code snippets for common security vulnerabilities aligned with 
    INCIBE guidelines and OWASP top 10 (e.g., hardcoded secrets, SQLi).
    """
    risks = []
    
    # 1. Hardcoded Secrets (API Keys, Passwords, Tokens)
    # Catches patterns like api_key = "12345" or SECRET="abcd"
    if re.search(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]", code_snippet):
        risks.append("Hardcoded secret or credential detected. Must use environment variables or a secure vault.")
        
    # 2. SQL Injection Risks (Raw string concatenation/f-strings in queries)
    # Catches patterns like f"SELECT * FROM users WHERE id = {user_id}"
    if re.search(r"(?i)SELECT.*FROM.*WHERE.*(%s|\+)", code_snippet) or re.search(r"(?i)f['\"]SELECT.*{.*}", code_snippet):
        risks.append("Potential SQL Injection detected. Strict parameterized queries must be used.")
        
    # 3. Insecure Cryptography / Deprecated Modules
    # Flags weak hashing or unencrypted protocols
    insecure_modules = ["hashlib.md5", "telnetlib", "ftp"]
    found_modules = [mod for mod in insecure_modules if mod in code_snippet.lower()]
    if found_modules:
        risks.append(f"Insecure or deprecated modules detected: {', '.join(found_modules)}. Use modern, secure alternatives (e.g., SHA-256, SSH, SFTP).")
        
    # 4. Format and return the payload to the Supervisor
    response = {
        "status": "SAFE",
        "agent": "Cybersecurity Agent",
        "analysis": {}
    }

    if risks:
        response["status"] = "HIGH_RISK"
        response["analysis"] = {
            "warning": "Critical security vulnerabilities found in the proposed code.",
            "vulnerabilities": risks,
            "recommendation": "Route to HITL Gateway immediately. Do not execute."
        }
        
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()