# 🕊️ UN Digital Peacekeepers (UNDPK) - AI Governance Orchestrator (Agent_Trace)

![UN Digital Peacekeepers](https://img.shields.io/badge/AI%20Governance-Enterprise-blue) ![Protocol](https://img.shields.io/badge/Protocol-MCP-green) ![Compliance](https://img.shields.io/badge/Compliance-EU%20AI%20Act%20%7C%20AESIA-orange) ![Challenge](https://img.shields.io/badge/SpainGov-UN%20Tech%20Over%202026-purple)

An enterprise-grade, Multi-Agent AI Governance Orchestrator built on the Model Context Protocol (MCP). Designed specifically for the **SpainGov Challenge — UN Tech Over 2026**, this system intercepts, evaluates, and legally grounds AI development before a single line of high-risk code or biased model is deployed.

---

## 🏆 The Core Innovation: Solving the Autonomous Governance Gap
Modern coding agents (OpenCode, Cline, Aider) prioritize speed over compliance. This architecture introduces a **Separation of Concerns** using discrete, deterministic Python Specialist Agents routed by a Supervisor LLM. 

It implements the challenge's four mandatory stages:
1. **Evaluate:** A semantic Fork Detector halts prompts modifying protected attributes, ML models, or fairness metrics.
2. **Present trade-off:** It calculates mathematical and compliance trade-offs, presenting explicit Options (A, B, C) to the developer.
3. **Store:** Records the Human-In-The-Loop (HITL) decision in an append-only, SHA-256 hash-chained `decisions.jsonl` ledger.
4. **Transform:** Converts cryptographic logs into an AESIA/EU AI Act-compliant human-readable Model Card.

---

## 🏗️ System Architecture & MCP Specialists

This project is fully provider-agnostic. The Supervisor handles semantic intent, while the following local `FastMCP` servers enforce hard constraints:

### ⚖️ 1. Fairness Agent (The Auditor)
*Utilizing `Fairlearn` and `scikit-learn` for live matrix mathematics.*
Evaluates models against the **Impossibility Theorem of Fairness**, proving all three cannot be satisfied simultaneously, and forces a developer choice between:
* **Predictive Parity (Northpointe):** Equal Precision / Positive Predictive Value across groups.
* **Equalized Odds (ProPublica):** Equal False Positive/Negative rates across groups.
* **Demographic Parity (Equality of Outcome):** Equal selection rates, ignoring historical base rates.

### 🔒 2. Privacy Agent (The Guardian)
*Grounded in AESIA Guide 7 & GDPR Article 5.*
* Scans schemas for protected attributes (PII, PHI).
* Detects the **Proxy Variable Trap**: Warns developers that simply deleting a "Race" column while keeping "Zip Code" enables the model to reverse-engineer protected classes, violating anti-discrimination law.

### 🛡️ 3. Cyber Agent (The Shield)
*Grounded in AESIA Guide 11.*
* Actively detects cognitive hacking (Cialdini’s principles of persuasion, artificial urgency) to prevent semantic jailbreaks.
* Evaluates generated code for insecure default states and model-inversion vulnerabilities.

### 📜 4. The Cryptographic Audit Agent & HITL Gateway
Resolves the workshop's "Audit Log Paradox" (strict immutability vs. log bloat). Uses an append-only `decisions.jsonl` chain where corrections utilize a `supersedes_hash` flag. The original human error remains cryptographically intact, but the active state is safely updated.

---

## 🚀 Getting Started (Local Deployment)

### Prerequisites
* Python 3.9+
* OpenCode IDE (or any standard MCP-compatible client)

### Installation
1. Clone the repository and navigate to the project root.
2. Create and activate a clean virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # Windows: venv\Scripts\activate
