from mcp.server.fastmcp import FastMCP
# import re
import json

#This cybersecurity agent is designed to provide real-time vulnerability scanning and prompt injection detection for any code snippets or user prompts processed by the system. It serves as a proactive defense layer, identifying potential security risks before they can be exploited, and ensuring that the AI operates within safe parameters.
#It also looks for hardcoded secrets, potential SQL injection patterns, and the use of deprecated or insecure modules in code snippets. For user prompts, it detects common jailbreak techniques such as authority overrides, urgency manipulation, academic framing, and obfuscation attempts. The agent provides detailed feedback on any risks detected, allowing for informed decision-making on whether to proceed with processing or to reject the input for security reasons.
#It also looks out for prompt injection attacks, cognitive hacking attempts, and Cialdini-based persuasion techniques that could be used to bypass safety filters. By analyzing the content of user prompts for patterns indicative of adversarial manipulation, the agent can flag high-risk inputs and recommend appropriate actions to mitigate potential threats.
#Governance Mapping: The agent maps detected adversarial tactics to established AI governance frameworks such as NIST AI RMF, ISO/IEC 42001, and the EU AI Act. This mapping provides a clear classification of the violation type and its implications for AI safety and compliance, enabling organizations to understand the severity of the risk and take appropriate measures to address it.


mcp = FastMCP("Cybersecurity Agent")

@mcp.tool()
def map_adversarial_intent(detected_tactic: str, user_justification: str) -> str:
    """
    Maps a semantically detected persuasion tactic to its official 
    AI Governance risk framework classification.
    """
    # The taxonomy of Cialdini / Adversarial attacks mapped to Governance
    taxonomy = {
        "authority": {
            "framework": "NIST AI RMF (Safety & Robustness Pillar)",
            "violation_type": "Cognitive Hacking via Authority Illusion",
            "description": "User attempted to leverage a fabricated high-status role, professional credential, or administrative status to override alignment safeguards."
        },
        "urgency": {
            "framework": "ISO/IEC 42001 (AI Risk Assessment)",
            "violation_type": "Artificial Urgency Manipulation",
            "description": "User generated a false high-stakes crisis or time-critical emergency to trick the system into skipping deep inspection gates."
        },
        "scarcity_or_exclusivity": {
            "framework": "NIST AI RMF",
            "violation_type": "Exclusivity Bypass",
            "description": "User implied the request is a unique, highly restricted, or privileged exception to safety rules."
        },
        "implied_discrimination": {
            "framework": "EU AI Act - Article 5 (Prohibited AI Practices)",
            "violation_type": "Subtle/Proxy Algorithmic Discrimination",
            "description": "The prompt contains semantic indicators of demographic profiling, proxy variables for protected attributes, or predictive policing intent, which is strictly prohibited."
        }
    }

    tactic_key = detected_tactic.lower().strip()
    match = taxonomy.get(tactic_key, {
        "framework": "General AI Governance Guidelines",
        "violation_type": "Unclassified Semantic Anomaly",
        "description": "The system detected an adversarial framing attempt designed to bypass standard operational boundaries."
    })

    return json.dumps({
        "status": "PROHIBITED",
        "governance_mapping": match
    }, indent=2)

if __name__ == "__main__":
    mcp.run()