# 🤖 Autonomous Portfolio Rebalancing Agent

An autonomous, multi-agent financial portfolio rebalancing platform built with Python and Streamlit. The system features dynamic drift calculations, convex optimization via `cvxpy`, Explainable AI (XAI) using Tree SHAP and counterfactual analysis, regulatory audit logging, and an emergency System Kill-Switch.

---

## 🌟 Key Features

* **Multi-Agent Architecture**: Dedicated virtual specialists (`Portfolio Analyst`, `Risk Manager`, `Tax Specialist`, `Compliance Officer`, `Explanation Writer`) coordinated by a master Orchestrator.
* **Mathematical Optimization Engine**: Real-time drift calculation, transaction cost modeling, and convex optimization via `cvxpy`.
* **Explainable AI (XAI)**: Native integration with `SHAP` and `LIME` to generate transparent, auditable explanations for advisors and compliance teams.
* **Safety & Override Mechanisms**: Automated risk triggers, escalation management, human-in-the-loop override capture, and an emergency **System Kill Switch**.
* **Backtesting & Analytics**: Historical strategy simulation, scenario testing, and performance metrics (Sharpe ratio, max drawdown, CVaR).

---

## 🏗 System Architecture

```text
+-----------------------------------------------------------------------+
|                         ORCHESTRATOR AGENT                          |
|               (Central Controller & Workflow Lead)                 |
+-----------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                         |                         |
         v                         v                         v
+------------------+     +------------------+     +------------------+
| Portfolio Analyst|     |   Risk Manager   |     |  Tax Specialist  |
+------------------+     +------------------+     +------------------+
         |                         |                         |
         +-------------------------+-------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+------------------+                               +------------------+
|Compliance Officer|                               |Explanation Writer|
+------------------+                               +------------------+
         |                                                   |
         v                                                   v
+------------------+                               +------------------+
| MATH & OPT ENGINE|                               | AI EXPLAINABILITY|
| Drift / Optimizer|                               |   SHAP & LIME    |
+------------------+                               +------------------+
         |                                                   |
         +-------------------------+-------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                     SAFETY & OVERRIDE LAYER                       |
|            (System Kill Switch | Human Override Engine)             |
+-----------------------------------------------------------------------+

📁 Repository Structure
autonomous-portfolio-agent/
│
├── agents/                 # Multi-agent specialized workforce
│   ├── compliance_officer.py
│   ├── explanation_writer.py
│   ├── orchestrator.py
│   ├── portfolio_analyst.py
│   ├── risk_manager.py
│   └── tax_specialist.py
│
├── backtesting/            # Historical strategy execution and analytics
│   ├── back_test_engine.py
│   ├── performance_analyser.py
│   ├── scenario_runner.py
│   └── strategy_comparator.py
│
├── compliance/             # Regulatory, bias, and scorecard audits
│   ├── bias_detector.py
│   ├── compliance_auditor.py
│   ├── explainability_scorecard.py
│   └── regulatory_reporter.py
│
├── dashboard/              # Streamlit multi-page UI
│   ├── pages/
│   │   ├── 1_portfolio_overview.py
│   │   ├── 2_rebalancing_activity.py
│   │   ├── 3_performance_analytics.py
│   │   ├── 4_explainability_centre.py
│   │   └── 5_system_health.py
│   └── app.py
│
├── data/                   # Market metadata, synthetic generators, & tax trackers
│   ├── asset_universe.py
│   ├── client_constraints.py
│   ├── synthetic_portfolio_generator.py
│   └── tax_lock_tracker.py
│
├── engine/                 # Core math, drift, and optimization routines
│   ├── cost_impact_model.py
│   ├── cvxpy_optimizer.py
│   ├── drift_calculator.py
│   └── trigger_evaluator.py
│
├── explainability/         # Model transparency & feature importance
│   ├── advisor_explainer.py
│   ├── client_explainer.py
│   ├── compliance_explainer.py
│   ├── counter_factual_generator.py
│   ├── explanation_generator.py
│   ├── lime_integration.py
│   └── shap_integration.py
│
├── overide/                # Safety switches and escalation management
│   ├── escalation_manager.py
│   ├── intervention_classifier.py
│   ├── kill_switch.py
│   └── override_capture.py
│
└── tests/                  # Test suite for unit and integration coverage
    ├── test_agent.py
    ├── test_backtesting.py
    ├── test_data.py
    ├── test_engine.py
    ├── test_explainability.py
    └── test_override.py


🚀 Quickstart Guide
Prerequisites
Python 3.10+

Virtual environment tool (venv or conda)

1. Installation & Environment Setup
Clone the repository and navigate into the project directory:
git clone [https://github.com/your-username/autonomous-portfolio-agent.git](https://github.com/your-username/autonomous-portfolio-agent.git)
cd autonomous-portfolio-agent

Create and activate a virtual environment:
# On Linux/macOS
python -m venv .venv
source .venv/bin/activate

# On Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

Install standard project dependencies:
pip install -r requirements.txt

2. Launching the Interactive Dashboard
Launch the multi-page Streamlit dashboard:
streamlit run dashboard/app.py

🧪 Verification & Testing
The repository includes complete test suites covering agent orchestration, SHAP feature attributions, counterfactual generation, and safety kill-switch states.

Run Unit Tests & Coverage
Run pytest to execute all 13 test cases across modules:
pytest --cov=agents --cov=backtesting --cov=compliance --cov=data --cov=engine --cov=explainability --cov=overide tests/

To suppress third-party deprecation warnings (e.g., SHAP/matplotlib):
pytest -W ignore::PendingDeprecationWarning --cov=agents --cov=backtesting --cov=compliance --cov=data --cov=engine --cov=explainability --cov=overide tests/

Format Codebase
To enforce standard PEP 8 formatting across all scripts using black:
black .

🛡️ Risk & Safety Controls
System Kill Switch: Global safety mechanism mediated via st.session_state["kill_switch_active"] and overide.kill_switch.SystemKillSwitch. Automatically halts execution cycles when VIX or error rates breach set bounds.

Human-in-the-Loop Override: HumanOverrideEngine logs advisor intervention decisions and captures explicit approvals for flagged portfolio actions.

Regulatory Compliance: Every decision cycle is recorded through compliance_auditor.py to maintain a deterministic audit log for compliance scorecards.
