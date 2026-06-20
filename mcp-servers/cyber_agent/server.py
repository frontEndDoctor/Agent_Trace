from mcp.server.fastmcp import FastMCP
import re
import json

#This cybersecurity agent is designed to provide real-time vulnerability scanning and prompt injection detection for any code snippets or user prompts processed by the system. It serves as a proactive defense layer, identifying potential security risks before they can be exploited, and ensuring that the AI operates within safe parameters.
#It also looks for hardcoded secrets, potential SQL injection patterns, and the use of deprecated or insecure modules in code snippets. For user prompts, it detects common jailbreak techniques such as authority overrides, urgency manipulation, academic framing, and obfuscation attempts. The agent provides detailed feedback on any risks detected, allowing for informed decision-making on whether to proceed with processing or to reject the input for security reasons.
#It also looks out for prompt injection attacks, cognitive hacking attempts, and Cialdini-based persuasion techniques that could be used to bypass safety filters. By analyzing the content of user prompts for patterns indicative of adversarial manipulation, the agent can flag high-risk inputs and recommend appropriate actions to mitigate potential threats.

mcp = FastMCP("Cybersecurity Agent")

@mcp.tool()
def scan_for_vulnerabilities(code_snippet: str) -> str:
    """Scans code for hardcoded secrets, SQLi, and deprecated modules."""
    risks = []
    if re.search(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]", code_snippet):
        risks.append("Hardcoded secret detected.")
    if re.search(r"(?i)SELECT.*FROM.*WHERE.*(%s|\+)", code_snippet) or re.search(r"(?i)f['\"]SELECT.*{.*}", code_snippet):
        risks.append("Potential SQL Injection detected.")
    
    insecure_modules = ["hashlib.md5", "telnetlib", "ftp"]
    found_modules = [mod for mod in insecure_modules if mod in code_snippet.lower()]
    if found_modules:
        risks.append(f"Insecure modules detected: {', '.join(found_modules)}.")
        
    return json.dumps({"status": "HIGH_RISK" if risks else "SAFE", "risks": risks})

# --- JAILBREAK DETECTOR TOOL ---

@mcp.tool()
def scan_for_prompt_injection(user_prompt: str) -> str:
    """
    Scans the raw user prompt for adversarial AI attacks, cognitive hacking, 
    and Cialdini-based persuasion jailbreaks.
    """
    flags = []
    prompt_lower = user_prompt.lower()

    # 1. Authority / Roleplay Override (The Developer Mode attack)
    authority_patterns = [r"ignore previous instructions", r"you are now.*(developer|unrestricted)", r"bypass.*guardrails"]
    if any(re.search(p, prompt_lower) for p in authority_patterns):
        flags.append("Authority Override: Attempt to redefine system identity or ignore core instructions.")

    # 2. Urgency / Scarcity (Forcing the AI to skip safety checks)
    urgency_patterns = [r"life or death", r"emergency", r"do this immediately without.*warning"]
    if any(re.search(p, prompt_lower) for p in authority_patterns):
        flags.append("Urgency Manipulation: Exploiting time-sensitivity to bypass safety filters.")

    # 3. Context Redefinition / Framing (Academic or Hypothetical bypass)
    if "for educational purposes only" in prompt_lower or "hypothetical scenario" in prompt_lower:
        # We don't strictly block all hypotheticals, but we flag them for high-risk targets
        flags.append("Academic/Hypothetical Framing: Potential attempt to legitimize restricted content generation.")

    # 4. Encoding / Obfuscation (Sneaking payloads in Base64 or Hex)
    # Matches basic Base64 strings that might hide malicious commands
    if re.search(r"(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", user_prompt):
        flags.append("Obfuscation Detected: Suspicious encoded string found. Potential payload concealment.")

    response = {
        "status": "SAFE",
        "agent": "Adversarial Firewall",
        "analysis": {}
    }

    if flags:
        response["status"] = "HIGH_RISK"
        response["analysis"] = {
            "warning": "Prompt Injection or Cognitive Hacking attempt detected.",
            "attack_vectors": flags,
            "recommendation": "Reject prompt. Do not process the user's request. Route to Audit Logger."
        }
        
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()