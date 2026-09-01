# System Architecture Specification

## Overview
The Autonomous Portfolio Rebalancing System automatically monitors portfolio drift, calculates tax-efficient trade executions using quadratic optimization, generates multi-stakeholder explanations (XAI), and enforces regulatory compliance.

+-------------------+     +---------------------+     +----------------------+
|  Data / Portfolios| --> |   Engine (CVXPY)    | --> | Compliance & Audit   |
+-------------------+     +---------------------+     +----------------------+
|                            |
v                            v
+-------------------+        +--------------------+
| Agents Pipeline   |        | Streamlit Dashboard|
+-------------------+        +--------------------+


---

## Key Subsystems

### 1. Engine (`engine/`)
* **`drift_calculator.py`**: Computes weight deviations and max drift against target allocations.
* **`cvxpy_optimizer.py`**: Solves convex portfolio optimization subject to turnover and tracking error constraints.
* **`cost_impact_model.py`**: Estimates linear brokerage and non-linear market impact costs.
* **`trigger_evaluator.py`**: Evaluates threshold, calendar, and market shock triggers.

### 2. Multi-Agent System (`agents/`)
* **`orchestrator.py`**: Coordinates workflow execution across all sub-agents.
* **`portfolio_analyst.py`**: Analyzes risk profile and benchmark relative returns.
* **`tax_specialist.py`**: Evaluates Short-Term Capital Gains (STCG) vs Long-Term Capital Gains (LTCG) tax implications.
* **`compliance_officer.py`**: Audits single-asset concentration and sanctions rules.
* **`explanation_writer.py`**: Synthesizes persona-based explanations.

### 3. Explainability (`explainability/`)
* Uses **SHAP** and **LIME** attributions to identify feature importance driving trade decisions.
* Generates counterfactual ("what-if") scenarios evaluating portfolio state without rebalancing.

### 4. Human-in-the-Loop & Overrides (`override/`)
* **`kill_switch.py`**: System-wide circuit breaker triggered by market volatility (VIX breaches) or error rates.
* **`escalation_manager.py`**: Routes high-risk or flagged trade recommendations to human advisors.