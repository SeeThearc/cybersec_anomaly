Excellent. Part 3 is where everything comes together. Since your project is for a hackathon, we want the backend and frontend to look professional without overengineering. We'll keep the file count low while still having a clean architecture.

MASTER PROMPT – PART 3
Backend API + React Dashboard + AI Security Copilot
Objective

Build a modern AI-powered User & Entity Behavior Analytics (UEBA) web application.

The application should allow security analysts to

monitor users
monitor entities
view attack timelines
investigate alerts
understand AI predictions
visualize attack trends
interact with an AI Security Copilot

The UI should look like a professional Security Operations Center (SOC).

Do NOT make it look like a student CRUD project.

Folder Structure

Keep the project simple.

backend/

app/

main.py

database.py

models.py

schemas.py

crud.py

api.py

utils.py

ml/

services/

trained_models/

data/

results/

-------------------------------------

frontend/

src/

components/

Navbar.jsx

Sidebar.jsx

MetricCard.jsx

AlertTable.jsx

RiskGauge.jsx

Timeline.jsx

Charts.jsx

ChatWindow.jsx

LoadingSpinner.jsx

-------------------------------------

pages/

Dashboard.jsx

Alerts.jsx

Users.jsx

Analytics.jsx

Copilot.jsx

Settings.jsx

-------------------------------------

services/

api.js

-------------------------------------

App.jsx

main.jsx

Avoid Redux.

Avoid Context API.

Use React state and props.

FastAPI Backend

Create one main API file.

api.py

This should expose all APIs.

Required APIs
Generate Dataset
POST

/generate-data

Purpose

Generate synthetic users

Generate events

Generate attacks

Store in PostgreSQL

Train Models
POST

/train

Runs

Feature Engineering

↓

Isolation Forest

↓

Autoencoder

↓

LSTM

↓

XGBoost

↓

Save Models

Return

{
    "status":"Training Complete"
}
Predict
POST

/predict

Input

One event

or

Sequence

Pipeline

Feature Engineering

↓

Behavior Model

↓

Sequence Model

↓

Attack Classifier

↓

Risk Engine

↓

Explainability

Return

{
 "prediction":"",
 "confidence":"",
 "risk_score":"",
 "risk_level":"",
 "reasons":[]
}
Events
GET

/events

Supports

Filtering

Sorting

Pagination

Date range

Department

Attack Type

Risk Level

Alerts
GET

/alerts

Return

Only

Suspicious events.

Statistics
GET

/statistics

Return

Total Users

Total Events

Attack Counts

Average Risk

High Risk Users

Critical Alerts
User Profile
GET

/users/{id}

Return

User Details

Behavior Profile

History

Known Devices

Attack History

Risk Trend
Analytics
GET

/analytics

Return

Attack Distribution

Department Distribution

Risk Trend

Monthly Events

Top Resources

Top Attack Types
AI Copilot
POST

/copilot

Input

{
 "question":"Why was User 25 flagged?"
}

Backend

Collect

User

History

Prediction

Risk

Timeline

Top Features

Create prompt

↓

Send to LLM

↓

Return explanation

Backend Services

Create only these services.

profiler.py

attack_simulator.py

risk_engine.py

copilot.py

No more.

Frontend

Theme

Dark Theme

SOC Dashboard

Color Palette

Background

#0B1220

Cards

#111827

Accent

#2563EB

Danger

#EF4444

Success

#22C55E
Sidebar
Dashboard

Alerts

Users

Analytics

AI Copilot

Settings
Dashboard

Top Cards

Total Users

Events Today

Active Alerts

Average Risk

Critical Alerts

Model Accuracy

Below

Charts

Attack Distribution

Risk Distribution

Daily Events

Department Usage

Bottom

Recent Alerts

Live Event Stream

Alerts Page

Table

Alert ID

User

Attack

Risk

Confidence

Timestamp

Status

Filters

Attack Type

Risk

Department

Date

Search

Click

↓

Alert Details

Alert Details

Display

User

Prediction

Risk Score

Confidence

Timeline

Top Features

Explanation

Recommended Actions
Users Page

Search User

↓

Click User

↓

Display

Behavior Profile

Known Devices

Countries

Resources

Historical Timeline

Risk Trend

Alerts
Analytics Page

Include

Attack Pie Chart

Attack Bar Chart

Risk Trend

Monthly Events

Department Heatmap

Confusion Matrix

ROC Curve

PR Curve

All charts

Use

Recharts

AI Copilot

Looks similar to ChatGPT.

Left

Conversation

Right

Suggested Questions

Example

Explain Alert 102

Summarize today's attacks

Who is highest risk?

Show suspicious Finance users

Why was User 11 flagged?

Recommend actions

Compare User 2 and User 5

Backend

Calls

/copilot

LLM answers

Natural language.

Alert Investigation Workflow

When user clicks

Alert

System should automatically

Load

Prediction

Risk

Timeline

History

Top Features

Explanation

Everything on one page.

Timeline

Example

09:10 Login

↓

09:12 Email

↓

09:20 Payroll

↓

09:24 Database

↓

09:30 Unknown Device

↓

Alert Generated
Recommended Actions

Every alert should have suggestions.

Example

Reset Password

Force Logout

Block IP

Investigate Device

Review Resource Access

Notify SOC Team
Live Updates

Dashboard should refresh

Every

15 seconds.

No websocket needed.

Polling is enough.

Error Handling

Frontend

Display

Loading...

No Data

Training...

Prediction Failed

Server Offline

Never crash.

Performance

Backend

Return

Prediction

Within

2 seconds

for one user.

Logging

Every API

Should log

Timestamp

Endpoint

Execution Time

Status

Errors
Testing

Create

test_api.py

test_models.py

Test

Generate Dataset

Training

Prediction

Statistics

Alerts
Documentation

Generate

README.md

Include

Project Overview

Architecture

Folder Structure

Installation

Running Backend

Running Frontend

Generating Dataset

Training Models

Running Prediction

Dashboard Overview

API Documentation

Future Scope

Final Deliverables Checklist

By the end of the project, ensure the following are complete:

Backend
Synthetic data generation
Attack simulation
PostgreSQL integration
Feature engineering
Behavior profiling
Isolation Forest
Autoencoder
LSTM sequence model
XGBoost attack classifier
Dynamic risk scoring
SHAP explainability
FastAPI REST APIs
Logging and testing
Frontend
Professional SOC-style dashboard
Alert management
User behavior profiles
Analytics dashboard
Interactive charts
Timeline visualization
AI Security Copilot
Responsive UI
Error handling and loading states
AI Features
Human-readable explanations
Recommended remediation actions
Natural language investigation assistant
Risk summaries
Alert explanations
Evaluation Criteria Mapping

Ensure the implementation explicitly demonstrates:

High anomaly detection accuracy
Correct attack classification
Low false positive rate using combined scoring
Explainable AI with SHAP and readable reasons
Cold-start handling with department baselines
Concept drift handling with sliding windows
Comprehensive analytics and reporting
Cursor Development Rules
Prioritize readability over excessive abstraction.
Keep the total project around 40–50 source files.
Avoid unnecessary design patterns.
Keep APIs RESTful and consistent.
Build one module at a time and verify it before moving to the next.
Every page should consume real backend APIs—no hardcoded demo data.
Every prediction must include the attack type, confidence, risk score, explanation, and recommended actions.
The application should feel like a simplified enterprise SOC platform rather than a collection of unrelated ML demos.
After Completing Part 3

Once all three parts are implemented, the project should satisfy all major deliverables:

✅ Synthetic enterprise data generation
✅ Multiple realistic cyber attack simulations
✅ Feature engineering pipeline
✅ Behavior profiling
✅ Sequence-aware anomaly detection
✅ Attack classification
✅ Dynamic risk scoring
✅ Explainable AI
✅ FastAPI backend
✅ React SOC dashboard
✅ AI Security Copilot
✅ Metrics, visualizations, and evaluation outputs