from mcp.server.fastmcp import FastMCP
import re
import json

#This runtime monitor is designed to be a dynamic firewall that intercepts the generated output from the LLM before it is rendered to the human user. It detects potential hallucinations, accidental PII leaks, or leaked system prompts, and can sanitize the output in real-time while providing detailed feedback on any anomalies detected.
mcp = FastMCP("Runtime Guardrails")

@mcp.tool()
def intercept_output_stream(raw_llm_output: str) -> str:
    """
    Acts as a dynamic runtime firewall intercepting generated output 
    before it is rendered to the human user. Detects hallucinations, 
    accidental PII leaks, or leaked system prompts.
    """
    flags = []
    sanitized_output = raw_llm_output
    
    # 1. Output Data Loss Prevention (DLP)
    # If the model hallucinates or accidentally leaks a high-risk secret key in its response
    secret_patterns = {
        "AWS_KEY": r"AKIA[0-9A-Z]{16}",
        "GENERIC_SECRET": r"(?i)secret[-_]?key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]"
    }
    
    for key_type, pattern in secret_patterns.items():
        if re.search(pattern, raw_llm_output):
            flags.append(f"DLP Breach: Model attempted to emit a live credential ({key_type}).")
            # Redact the token at runtime
            sanitized_output = re.sub(pattern, "[REDACTED_SECURITY_BYPASS]", sanitized_output)

    # 2. System Prompt Leak / Meta-Instruction Leak
    # If the model starts printing out its own identity instructions ("You are the Supervisor Agent...")
    if "you are the supervisor agent" in raw_llm_output.lower() or "identity" in raw_llm_output.lower() and "orchestrator" in raw_llm_output.lower():
        flags.append("System Prompt Extraction: Model attempted to leak its core system prompt instructions.")
        sanitized_output = "Error: Execution halted due to internal safety guardrail policy violation."

    # 3. Model Denial of Wallet / Infinite Loop Detection
    # If a response contains an excessive repetition pattern indicative of a broken model state
    # (e.g., repeating the same word 10+ times in a row)
    if re.search(r"(\b\w+\b)( \1){9,}", raw_llm_output):
        flags.append("Model State Loop Detection: Detected catastrophic repetition/infinite loop anomaly.")
        sanitized_output = "[Runtime Monitor Alert: Execution terminated due to generation instability.]"

    response = {
        "status": "APPROVED" if not flags else "INTERCEPTED",
        "monitor_type": "Dynamic Output Stream Guard",
        "anomalies_detected": flags,
        "payload_delivered": sanitized_output
    }
    
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()