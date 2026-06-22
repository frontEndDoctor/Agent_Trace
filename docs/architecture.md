import os

markdown_content = """# 🏛️ UN Digital Peacekeepers (UNDPK) - System Architecture

This document outlines the architecture for the **UN Digital Peacekeepers**, a proactive AI governance orchestrator built on the Model Context Protocol (MCP). 

## 1. System Overview
The UNDPK architecture acts as a "Separation of Concerns" model. Rather than relying on a generalized LLM to guess legal compliance, a Supervisor LLM routes high-risk developer prompts to deterministic, specialized Python MCP servers. These servers evaluate AI code for legal compliance (EU AI Act, AESIA, GDPR) *before* it is ever written or deployed.

## 2. Architecture Diagram
un-digital-peacekeepers/
├── AGENTS.md                    # Core system prompt / Prime Directive
├── Auditor_Report.md            # The generated compliance report
├── README.md                    # GitLab default readme
├── UNPK README.md               # Hackathon submission documentation
├── credit_scoring_train.py      # User workspace file
├── decisions.jsonl              # Cryptographic audit ledger
├── generate_audit_report.py     # Script to generate markdown report
├── loan_fairness_eval.py        # User workspace file
├── opencode.json                # IDE Tool Configuration
├── requirements.txt             # Python dependencies
├── audit-trail/                 # Directory for auxiliary audit logs
├── venv/                        # Python virtual environment
└── mcp-servers/                 # The deterministic agent backends
    ├── audit_log/
    ├── cyber_agent/
    ├── fairness_agent/
    └── privacy_agent/

### 3. Core Components
🧠 The Supervisor Layer
AGENTS.md (The Prime Directive): The central rulebook that overrides the LLM's default coding behavior. It forces the AI to act as an auditor and consult the MCP tools before writing code.

Supervisor LLM: The IDE extension (OpenCode/Cline) that parses developer intent and coordinates with the underlying Python servers.

⚙️ The MCP Specialists (Python Servers)
Located within the mcp-servers/ directory:

privacy_agent: Active detection of GDPR "Proxy Variable Traps" (e.g., stopping developers from deleting 'Race' but keeping 'Zip Code').

fairness_agent: Executes live data science checks using Fairlearn to mathematically calculate parity and prove the Impossibility Theorem of Fairness under the EU AI Act.

cyber_agent: Acts as a cognitive firewall. Detects social engineering, artificial urgency, and blocks attempts to bypass security middleware (aligned with AESIA Guide 11).

🛡️ The Auditing & HITL Layer
Human-In-The-Loop (HITL) Gateway: The architectural pause. When an MCP tool flags a risk, the system halts and forces the developer to choose an option.

audit_log (MCP Server): Takes the developer's choice and generates a deterministic SHA-256 hash-chained entry.

decisions.jsonl: The immutable cryptographic ledger storing all governance decisions.

generate_audit_report.py: A deterministic script that translates the raw JSON lines into a human-readable regulatory report (Auditor_Report.md).