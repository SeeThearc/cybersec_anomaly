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
- [ ] Milestone 13 - FastAPI APIs
- [ ] Milestone 14 - React Dashboard
- [ ] Milestone 15 - Analytics Dashboard
- [ ] Milestone 16 - AI Security Copilot
- [ ] Milestone 17 - Testing
- [ ] Milestone 18 - Documentation
- [ ] Milestone 19 - Final Integration
- [ ] Milestone 20 - Final Evaluation

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

# Milestone 13 — FastAPI

## APIs

- [ ] POST /generate-data
- [ ] POST /train
- [ ] POST /predict
- [ ] GET /events
- [ ] GET /alerts
- [ ] GET /statistics
- [ ] GET /analytics
- [ ] GET /users/{id}
- [ ] POST /copilot

---

# Milestone 14 — Dashboard

## Layout

- [ ] Sidebar
- [ ] Navbar
- [ ] Responsive layout

---

## Dashboard

- [ ] Metric cards
- [ ] Alert table
- [ ] Risk gauge
- [ ] Timeline
- [ ] Live events

---

# Milestone 15 — Analytics

- [ ] Attack distribution
- [ ] Risk distribution
- [ ] Daily events
- [ ] Monthly events
- [ ] Department chart
- [ ] Confusion matrix
- [ ] ROC curve
- [ ] PR curve
- [ ] SHAP visualization

---

# Milestone 16 — AI Security Copilot

- [ ] Chat interface
- [ ] Backend endpoint
- [ ] Prompt generation
- [ ] Alert explanation
- [ ] User explanation
- [ ] Incident summary
- [ ] Recommended actions

---

# Milestone 17 — Testing

## Backend

- [ ] API testing
- [ ] Database testing
- [ ] Model testing
- [ ] Prediction testing

---

## Frontend

- [ ] Dashboard
- [ ] Charts
- [ ] API integration
- [ ] Error handling

---

# Milestone 18 — Documentation

- [ ] README
- [ ] Architecture diagram
- [ ] Folder structure
- [ ] API documentation
- [ ] Installation guide
- [ ] Usage guide

---

# Milestone 19 — Final Integration

- [ ] Backend connected
- [ ] Frontend connected
- [ ] Database connected
- [ ] Models connected
- [ ] Copilot connected

---

# Milestone 20 — Final Evaluation

## Deliverables

- [ ] Synthetic enterprise data generation
- [ ] Behavioral profiling
- [ ] Attack simulation
- [ ] Sequence-aware detection
- [ ] Attack classification
- [ ] Dynamic risk scoring
- [ ] Explainable AI
- [ ] FastAPI backend
- [ ] React dashboard
- [ ] AI Security Copilot

---

## Evaluation Criteria

- [ ] High anomaly detection accuracy
- [ ] Correct attack classification
- [ ] Low false positives
- [ ] Explainability
- [ ] Cold-start handling
- [ ] Concept drift handling
- [ ] Complete report

---

# Final Pre-Demo Checklist

## Backend

- [ ] No API errors
- [ ] All endpoints working
- [ ] Models loading correctly
- [ ] Database populated

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