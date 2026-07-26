# PROJECT_RULES.md

# AI-Driven User & Entity Behavior Analytics (UEBA) System
## Cursor Development Rules & Engineering Guidelines

---

# Objective

This document defines the engineering rules that MUST be followed throughout the project.

These rules are more important than generating code quickly.

The goal is to build a production-quality, hackathon-friendly project that is:

- clean
- modular
- easy to understand
- easy to extend
- easy to debug

Never sacrifice code quality for unnecessary complexity.

---

# Rule 1 — Simplicity First

Always prefer the simplest solution that satisfies the requirements.

DO NOT over-engineer.

Avoid unnecessary abstractions.

If a simple function solves the problem, do not create multiple classes or wrappers.

---

# Rule 2 — Keep Folder Structure Small

Do NOT create unnecessary folders.

Do NOT create folders like

- managers
- handlers
- repositories
- interfaces
- factories
- adapters
- providers

unless absolutely necessary.

The entire project should remain around **40–50 source files**.

---

# Rule 3 — One Responsibility Per File

Each file should have one clear purpose.

Example

feature_engineering.py

Only feature engineering.

NOT

training

prediction

database logic

---

behavior_model.py

Only behavior profiling.

NOT

API logic.

---

api.py

Only API endpoints.

No ML code.

---

# Rule 4 — Never Duplicate Logic

If functionality already exists,

reuse it.

Never copy-paste functions.

Never create

predict2.py

predict_final.py

predict_new.py

etc.

Refactor instead.

---

# Rule 5 — Keep APIs RESTful

Every endpoint should have one responsibility.

Example

POST /generate-data

Only generates data.

---

POST /train

Only trains models.

---

POST /predict

Only predicts.

Do not combine multiple responsibilities into one endpoint.

---

# Rule 6 — Never Hardcode Values

Never hardcode

risk scores

thresholds

paths

credentials

database URLs

API keys

countries

departments

All configurable values should be constants or configuration variables.

---

# Rule 7 — Keep Code Readable

Prefer

```python
if risk_score > threshold:
    ...
```

instead of complicated one-line expressions.

Readable code is more important than clever code.

---

# Rule 8 — Use Type Hints

Every function should include type hints.

Example

```python
def calculate_risk(
    behavior_score: float,
    sequence_score: float
) -> float:
```

---

# Rule 9 — Write Small Functions

Prefer

20–40 line functions.

Avoid

300-line functions.

Split logic into helper functions.

---

# Rule 10 — Comment Important Logic

Do NOT comment every line.

Only explain

why

not

what.

Good

```python
# Isolation Forest only learns normal behavior
```

Bad

```python
# Increment i
i += 1
```

---

# Rule 11 — Naming Conventions

Use meaningful names.

Good

```python
behavior_score
```

Bad

```python
x
```

Good

```python
risk_level
```

Bad

```python
r
```

---

# Rule 12 — Database Rules

Never execute raw SQL unless necessary.

Always use SQLAlchemy.

Models should remain simple.

Relationships should be clear.

---

# Rule 13 — No Business Logic Inside Routes

Routes should only

receive request

↓

call service

↓

return response

Do NOT write ML logic inside FastAPI endpoints.

---

# Rule 14 — Separate ML Responsibilities

Each ML model has one responsibility.

Isolation Forest

↓

Behavior anomaly

Autoencoder

↓

Reconstruction error

LSTM

↓

Behavior sequence

XGBoost

↓

Attack classification

Risk Engine

↓

Risk score

SHAP

↓

Explainability

Never mix responsibilities.

---

# Rule 15 — Save Every Model

Training should happen once.

Models should be saved inside

trained_models/

Prediction should load saved models.

Do NOT retrain automatically.

---

# Rule 16 — Every Prediction Must Return

Prediction

Confidence

Risk Score

Risk Level

Explanation

Top Features

Recommended Actions

No exceptions.

---

# Rule 17 — Frontend Rules

Never hardcode dashboard values.

Everything should come from APIs.

Avoid duplicate components.

Keep UI clean.

Prefer reusable components.

---

# Rule 18 — Dashboard Style

Professional SOC Dashboard.

NOT

Student CRUD App.

Use

Dark Theme

Cards

Charts

Tables

Risk Indicators

Timeline

Alert Panels

---

# Rule 19 — Component Rules

Each component should do one thing.

MetricCard

Displays metric.

AlertTable

Displays alerts.

Timeline

Displays event sequence.

ChatWindow

Displays AI chat.

Do not combine unrelated UI.

---

# Rule 20 — State Management

Do NOT use Redux.

Do NOT use Context API.

Use React state.

Use props.

Keep it simple.

---

# Rule 21 — Error Handling

Every API call should handle

Loading

Empty State

Server Error

Timeout

Never allow the application to crash.

---

# Rule 22 — Logging

Every API request should log

Endpoint

Timestamp

Execution Time

Status

Errors

Training should also log progress.

---

# Rule 23 — Validation

Always validate

user IDs

timestamps

countries

devices

labels

session duration

before saving data.

---

# Rule 24 — Feature Engineering

Raw logs should never be fed directly into ML models.

Every prediction must pass through

Feature Engineering

first.

---

# Rule 25 — Synthetic Data

Synthetic data should look realistic.

Do NOT generate random meaningless values.

Every generated user should have

Working Hours

Preferred Resources

Known Devices

Country

Department

Typical Login Time

Average Session

Behavior should be consistent.

---

# Rule 26 — Attack Simulation

Attacks should simulate realistic enterprise threats.

Never inject random anomalies.

Each attack should follow a recognizable behavioral pattern.

---

# Rule 27 — Explainability

Every alert must explain

Why it happened.

Never return only

"Risk = 92"

Return reasons.

Example

✓ Login at unusual hour

✓ New country

✓ Unknown device

✓ Payroll accessed

---

# Rule 28 — Risk Scoring

Risk should combine

Behavior Score

Sequence Score

Classifier Confidence

Historical Risk

Never use only one model.

---

# Rule 29 — Cold Start

New users have no history.

Use department baseline.

Do not incorrectly classify them as malicious.

---

# Rule 30 — Concept Drift

User behavior changes.

Profiles should adapt.

Never assume behavior is fixed forever.

---

# Rule 31 — AI Copilot

The Copilot should

Explain alerts

Summarize incidents

Recommend actions

Answer analyst questions

It should never invent data.

It should only use information returned by the backend.

---

# Rule 32 — Reuse Existing Code

Before writing new code,

search the project.

If similar functionality exists,

reuse it.

Avoid duplicate utility functions.

---

# Rule 33 — Keep Dependencies Minimal

Do not install new libraries unless absolutely necessary.

Use the existing tech stack whenever possible.

---

# Rule 34 — Testing

Every completed module should be tested before moving to the next milestone.

Do not continue implementing features if the current milestone is broken.

---

# Rule 35 — Milestone Workflow

Never build the whole project at once.

Always work in this order.

1. Backend Setup

2. Database

3. Synthetic Data

4. Attack Simulation

5. Feature Engineering

6. Behavior Model

7. LSTM

8. XGBoost

9. Risk Engine

10. Explainability

11. APIs

12. Frontend

13. AI Copilot

14. Final Integration

Do not skip milestones.

---

# Rule 36 — Preserve Existing Code

Before modifying any file:

- Read the entire file first.
- Understand how it interacts with other modules.
- Make the smallest necessary change.
- Never rewrite a working file unless explicitly instructed.
- Avoid breaking existing APIs or function signatures.

---

# Rule 37 — Ask Before Major Refactoring

If a requested feature requires major architectural changes:

- Explain why.
- Propose the change.
- Wait for confirmation before refactoring.

Do not restructure the project on your own.

---

# Rule 38 — Code Quality

Every new piece of code should be:

- Modular
- Readable
- Type hinted
- Documented where necessary
- Consistent with the existing code style

Prefer maintainability over clever optimizations.

---

# Final Rule

Always remember the project goal.

This is **not** just an anomaly detector.

This is a complete AI-powered User & Entity Behavior Analytics (UEBA) platform that demonstrates:

- Synthetic enterprise data generation
- Behavioral profiling
- Sequence-aware anomaly detection
- Cyber attack classification
- Dynamic risk scoring
- Explainable AI
- FastAPI backend
- React SOC dashboard
- AI Security Copilot

Every implementation decision should move the project toward that goal while keeping the architecture simple, modular, and hackathon-friendly.