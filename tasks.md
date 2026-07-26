# TASKS.md

# AI-Driven User & Entity Behavior Analytics (UEBA)
## Project Development Checklist

---

# Project Progress

- [x] Milestone 1 - Project Setup
- [x] Milestone 2 - Database
- [x] Milestone 3 - Synthetic Data Generator
- [x] Milestone 4 - Attack Simulation
- [x] Milestone 5 - Feature Engineering
- [x] Milestone 6 - Behavior Profiling
- [x] Milestone 7 - Sequence Learning
- [x] Milestone 8 - Attack Classification
- [x] Milestone 9 - Risk Scoring
- [x] Milestone 10 - Explainability
- [x] Milestone 11 - Model Training Pipeline
- [x] Milestone 12 - Prediction Pipeline
- [x] Milestone 13 - FastAPI APIs
- [x] Milestone 14 - React Dashboard
- [x] Milestone 15 - Analytics Dashboard
- [x] Milestone 16 - AI Security Copilot
- [x] Milestone 17 - Testing
- [x] Milestone 18 - Documentation
- [x] Milestone 19 - Final Integration
- [x] Milestone 20 - Final Evaluation

---

# Milestone 1 — Project Setup

## Backend

- [x] Create FastAPI project
- [x] Configure virtual environment
- [x] Install dependencies
- [x] Create project folders
- [x] Configure environment variables
- [x] Configure PostgreSQL connection
- [x] Verify backend starts successfully

---

## Frontend

- [x] Create React project using Vite
- [x] Install TailwindCSS
- [x] Install Axios
- [x] Install Recharts
- [x] Configure routing
- [x] Create dark theme
- [x] Verify frontend runs

---

# Milestone 2 — Database

## SQLAlchemy Models

- [x] Users
- [x] Devices
- [x] Events
- [x] Alerts

---

## Database

- [x] Create tables
- [x] Test CRUD operations
- [x] Verify relationships
- [x] Seed sample records

---

# Milestone 3 — Synthetic Data Generator

## Employee Generator

- [x] Generate users
- [x] Generate departments
- [x] Generate roles
- [x] Generate countries
- [x] Generate work schedules
- [x] Generate login patterns

---

## Device Generator

- [x] Create devices
- [x] Assign fingerprints
- [x] Assign browsers
- [x] Assign operating systems

---

## Event Generator

- [x] Generate authentication logs
- [x] Generate access logs
- [x] Generate sessions
- [x] Generate uploads
- [x] Generate downloads
- [x] Generate command sequences

---

## Validation

- [x] Validate timestamps
- [x] Validate IDs
- [x] Validate countries
- [x] Validate sessions
- [x] Remove invalid rows

---

# Milestone 4 — Attack Simulation

## Normal Behavior

- [x] Build baseline behavior
- [x] Verify realistic sequences

---

## Brute Force

- [x] Failed login bursts
- [x] High login frequency
- [x] Same IP simulation

---

## Impossible Travel

- [x] Geo changes
- [x] Distance calculation
- [x] Travel speed calculation

---

## Credential Stuffing

- [x] Multiple users
- [x] Same IP
- [x] Failure bursts

---

## Device Spoofing

- [x] New device
- [x] Browser change
- [x] OS change
- [x] Fingerprint change

---

## Lateral Movement

- [x] Resource traversal
- [x] Privilege escalation
- [x] Server movement

---

## Low-and-Slow Exfiltration

- [x] Gradual downloads
- [x] Long-term trend

---

## Insider Drift

- [x] Role changes
- [x] Resource expansion
- [x] Behavioral adaptation

---

# Milestone 5 — Feature Engineering

## Time Features

- [x] Hour
- [x] Day
- [x] Month
- [x] Weekend
- [x] Working hours

---

## Login Features

- [x] Failed logins
- [x] Login frequency
- [x] Attempts per minute

---

## Device Features

- [x] Known device
- [x] Device change
- [x] Browser change
- [x] Fingerprint change

---

## Geo Features

- [x] Country change
- [x] Travel distance
- [x] Travel speed

---

## Resource Features

- [x] Resource diversity
- [x] Sensitive resource
- [x] First-time access

---

## Sequence Features

- [x] User sequences
- [x] Action encoding
- [x] Sequence windows

---

## Data Processing

- [x] Encoding
- [x] Scaling
- [x] Train split
- [x] Validation split
- [x] Test split

---

# Milestone 6 — Behavior Profiling

## Isolation Forest

- [x] Train model
- [x] Save model
- [x] Predict anomalies

---

## Autoencoder

- [x] Train model
- [x] Reconstruction error
- [x] Save model

---

## Combined Score

- [x] Normalize scores
- [x] Ensemble behavior score

---

# Milestone 7 — Sequence Learning

## Sequence Model

- [x] Sequence generation
- [x] Tokenization
- [x] LSTM

## Training & Validation

- [x] Training
- [x] Validation
- [x] Save model

---

# Milestone 8 — Attack Classification

## XGBoost Classifier

- [x] Train model
- [x] Feature vector input
- [x] Behavior score input
- [x] Sequence score input
- [x] Predict probabilities
- [x] Save model

---

## Classes

- [x] Normal
- [x] Brute Force
- [x] Credential Stuffing
- [x] Impossible Travel
- [x] Device Spoofing
- [x] Lateral Movement
- [x] Low-and-Slow Exfiltration
- [x] Insider Drift

---

# Milestone 9 — Risk Scoring

## Risk Engine

- [x] Behavior score weight
- [x] Sequence score weight
- [x] Classifier confidence weight
- [x] Historical risk weight

## Outputs

- [x] Risk score (0-100)
- [x] Risk level (Low/Medium/High/Critical)
- [x] Recommended actions

---

# Milestone 10 — Explainability

## SHAP

- [x] Feature importance
- [x] Summary values

---

## Human Explanation

- [x] Top reasons
- [x] Risk explanation
- [x] Recommended actions

---

# Milestone 11 — Model Training Pipeline

## Automation

- [x] Train isolation forest
- [x] Train autoencoder
- [x] Train LSTM
- [x] Train XGBoost
- [x] Save all models

## Evaluation

- [x] Confusion matrix
- [x] ROC curve
- [x] PR curve
- [x] Classification metrics
- [x] SHAP summary plot

---

# Milestone 12 — Prediction Pipeline

## Inference Engine

- [x] Load trained models
- [x] Extract features from raw JSON event
- [x] Predict behavior anomaly score
- [x] Predict sequence score
- [x] Run XGBoost classifier
- [x] Calculate risk score
- [x] Explain prediction with SHAP
- [x] Output standardized JSON response

---

# Milestone 13 — FastAPI APIs

## Routes

- [x] POST `/generate-data`
- [x] POST `/train`
- [x] POST `/predict`
- [x] GET `/events`
- [x] GET `/alerts`
- [x] GET `/statistics`
- [x] GET `/analytics`
- [x] GET `/users/{id}`
- [x] POST `/copilot`

## Copilot

- [x] Integrate AI Security Copilot service
- [x] Fallback offline stub implemented

---

# Milestone 14 — React Dashboard

## Layout Components

- [x] Setup TailwindCSS v4 with SOC theme
- [x] Implement API wrapper (`api.js`)
- [x] Sidebar navigation
- [x] Navbar with system status

## Dashboard View

- [x] Metric Cards (Total Users, Alerts, Risk)
- [x] Active Alerts Table
- [x] Risk Gauge Chart (Recharts)
- [x] Event Timeline
- [x] Auto-refresh data every 15s

---

# Milestone 15 — Analytics Dashboard

## Visualizations

- [x] Attack Distribution (Pie)
- [x] Risk Distribution (Area)
- [x] Department Chart (Bar)
- [x] Monthly Events (Bar)

## ML Model Evaluation

- [x] ROC Curve (Line)
- [x] Precision-Recall Curve (Line)
- [x] Confusion Matrix (Grid)
- [x] SHAP Feature Importance (Bar)

---

# Milestone 16 — AI Security Copilot

## Implementation

- [x] Chat UI
- [x] Backend endpoint
- [x] Prompt builder

## Copilot Skills

- [x] Incident summarization
- [x] Alert explanation
- [x] Recommended actions

## LLM Provider

- [x] Integrate with Gemini/OpenAI

---

# Milestone 17 — Testing

## Backend Tests (Pytest)

- [x] APIs (`test_api.py`)
- [x] Database (`test_db.py`)
- [x] Prediction Pipeline (`test_predict.py`)
- [x] Training Pipeline (`test_train.py`)

## Frontend Tests (Vitest)

- [x] Frontend API integration (`api.test.js`)
- [x] Dashboard UI components
- [x] Visualization rendering
- [x] Error handling

---

# Milestone 18 — Documentation

- [x] Update `README.md`
- [x] Architecture Diagram (Mermaid)
- [x] API documentation (Swagger/Redoc usage)
- [x] Installation guide
- [x] Usage guide
- [x] Future Scope

---

# Milestone 19 — Final Integration

- [x] Backend connected
- [x] Frontend connected
- [x] Database connected
- [x] Models connected
- [x] Copilot connected

---

# Milestone 20 — Final Evaluation

## Deliverables

- [x] Synthetic enterprise data generation
- [x] Behavioral profiling
- [x] Attack simulation
- [x] Sequence-aware detection
- [x] Attack classification
- [x] Dynamic risk scoring
- [x] Explainable AI
- [x] FastAPI backend
- [x] React dashboard
- [x] AI Security Copilot

---

## Evaluation Criteria

## Evaluation Criteria

- [x] High anomaly detection accuracy
- [x] Correct attack classification
- [x] Low false positives
- [x] Explainability
- [x] Cold-start handling
- [x] Concept drift handling
- [x] Complete report

---

# Final Pre-Demo Checklist

## Backend

- [x] No API errors
- [x] All endpoints working
- [x] Models loading correctly
- [x] Database populated

---

## Frontend

- [ ] Responsive UI
- [ ] Charts render correctly
- [ ] No dummy data
- [ ] No console errors

---

## ML

- [ ] Models trained
- [ ] Predictions working
- [ ] SHAP explanations generated
- [ ] Risk scores accurate

---

## Demo

- [ ] Generate synthetic data live
- [ ] Train models successfully
- [ ] Detect all attack types
- [ ] Display dashboard updates
- [ ] Explain an alert with AI Copilot
- [ ] Show analytics and metrics

---

# Definition of Done (DoD)

A milestone is considered complete only if:

- [ ] Code is implemented.
- [ ] Code is tested.
- [ ] No runtime errors.
- [ ] APIs return expected responses.
- [ ] Frontend is connected to backend.
- [ ] No hardcoded demo values.
- [ ] Existing functionality is not broken.
- [ ] Code follows PROJECT_RULES.md.