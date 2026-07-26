Excellent. This is the most important part of the project because it is what judges will evaluate the most.

One thing I'd improve from the previous design: don't make LSTM do everything. Each model should have one clear responsibility.

The pipeline should be:

Synthetic Data
        ↓
Feature Engineering
        ↓
Behavior Profiling (Isolation Forest + Autoencoder)
        ↓
Sequence Learning (LSTM)
        ↓
Attack Classification (XGBoost)
        ↓
Risk Scoring
        ↓
Explainability (SHAP + Rules)

This is easier to train, easier to explain to judges, and easier to debug.

MASTER PROMPT – PART 2
Machine Learning Pipeline
Objective

Build an AI-powered User & Entity Behavior Analytics (UEBA) pipeline capable of

learning normal user behavior
detecting anomalies
understanding behavioral sequences
classifying cyber attacks
generating risk scores
explaining every prediction

The system should be modular, where every ML model has a single responsibility.

Folder Structure

Keep it simple.

backend/

app/

ml/

data_generator.py

feature_engineering.py

behavior_model.py

sequence_model.py

classifier.py

risk_engine.py

explainability.py

train.py

predict.py

Avoid creating additional folders.

Complete Pipeline
Synthetic Dataset

↓

Feature Engineering

↓

Behavior Profiling

↓

Sequence Learning

↓

Attack Classification

↓

Risk Score

↓

Explainability

↓

FastAPI API

Every stage must be independent.

Feature Engineering

Create a dedicated module

feature_engineering.py

This module converts raw logs into ML features.

Time Features

Generate

Hour

Day

Weekend

Month

Working Hours

Session Duration

Time Since Previous Login
Authentication Features

Generate

Failed Login Count

Authentication Method

Success After Failures

Attempts Per Minute
Device Features

Generate

Device Changed

OS Changed

Browser Changed

Fingerprint Changed

Known Device
Geo Features

Generate

Country Changed

Distance Travelled

Travel Speed

Impossible Travel Flag
User Behaviour Features

Generate

Average Login Hour

Average Session

Average Downloads

Average Uploads

Resource Diversity

Unique Resources

Login Frequency

Historical Risk
Network Features

Generate

Unique IP Count

IP Reputation Score (synthetic)

VPN Flag

Private/Public Network
Resource Features

Generate

Sensitive Resource

First Time Access

Access Frequency

Resource Category
Sequence Features

Create ordered sequences.

Example

Login

↓

Email

↓

GitHub

↓

Database

↓

Logout

Store sequences per user.

Feature Scaling

Automatically

normalize numerical features
one-hot encode categorical features
label encode attack labels

Save preprocessing pipeline.

Behavior Profiling

Create

behavior_model.py

Purpose

Learn normal behavior only.

Do NOT classify attacks here.

Isolation Forest

Train using only

Normal

events.

Output

Anomaly Score

0–1
Autoencoder

Train only on

Normal users.

Objective

Learn compressed normal behavior.

Output

Reconstruction Error

Higher error

↓

More anomalous.

Combined Behavior Score

Combine

Isolation Forest

+

Autoencoder

Example

Behavior Score

=

0.6

Isolation Forest

+

0.4

Autoencoder

Return

Behavior Score

0–100
Sequence Learning

Create

sequence_model.py

Use

TensorFlow/Keras

Implement

LSTM

Purpose

Learn behavioral order.

Example

Normal

Login

↓

Email

↓

GitHub

↓

Logout

Attack

Login

↓

Payroll

↓

Database

↓

Admin

↓

Download

Convert

Actions

↓

Embeddings

↓

Sequences

↓

LSTM

Output

Sequence Score

0–100

Save model.

Attack Classification

Create

classifier.py

This model only classifies attacks.

Input

Behavior Score

+

Sequence Score

+

Feature Vector

Use

XGBoost

Output classes

Normal

BruteForce

CredentialStuffing

ImpossibleTravel

DeviceSpoofing

LateralMovement

LowSlowExfiltration

InsiderDrift

Return

Probability

for every class.

Example

Brute Force

93%

Credential Stuffing

3%

Device Spoofing

1%

Normal

3%
Risk Scoring Engine

Create

risk_engine.py

Input

Behavior Score

Sequence Score

Attack Probability

Historical Risk

Critical Resource

Compute

Risk Score

=

35%

Behavior Score

+

25%

Sequence Score

+

25%

Attack Confidence

+

15%

Historical Risk

Convert

0–30

LOW

31–60

MEDIUM

61–80

HIGH

81–100

CRITICAL

Return

Risk Score

Risk Level
Explainability

Create

explainability.py

Use

SHAP

Explain

Which features contributed most.

Return

Example

Risk Score

94

Top Reasons

✓ Login at unusual hour

✓ New Country

✓ New Device

✓ Accessed Payroll Database

✓ Multiple Failed Logins

Generate both

Machine explanation

and

Human explanation.

Cold Start Handling

Brand-new users

have

No history.

Instead of anomaly detection,

create

department baseline.

Example

Engineering

Typical Login

9–11 AM

Typical Resources

GitHub

Jira

Confluence

Use this baseline

until enough history exists.

Concept Drift

Behavior changes.

Implement

Sliding Window

Example

Last

30 days

instead of

Entire history.

Update

Behavior Profile

weekly.

False Positive Reduction

Never alert

using only one model.

Instead

Behavior Score

+

Sequence Score

+

Attack Confidence

must all exceed threshold.

Otherwise

mark

Needs Review

instead of

Attack
Model Training

Create

train.py

Automatically

Train

Isolation Forest

↓

Autoencoder

↓

LSTM

↓

XGBoost

Save

all models

inside

trained_models/
Prediction Pipeline

Create

predict.py

Pipeline

Input Event

↓

Feature Engineering

↓

Behavior Score

↓

Sequence Score

↓

Attack Classification

↓

Risk Score

↓

SHAP Explanation

↓

Return JSON
Output Format

Return

{
  "prediction": "CredentialStuffing",
  "confidence": 0.94,
  "behavior_score": 91,
  "sequence_score": 88,
  "risk_score": 92,
  "risk_level": "CRITICAL",
  "top_features": [
    "Failed Login Count",
    "New Country",
    "Unknown Device"
  ],
  "explanation": "The user logged in from an unknown device in a new country after multiple failed login attempts. The sequence strongly resembles credential stuffing."
}
Evaluation Metrics

Automatically compute

Classification

Accuracy

Precision

Recall

F1 Score

Confusion Matrix

Anomaly Detection

ROC AUC

PR AUC

False Positive Rate

False Negative Rate

Sequence Model

Validation Loss

Training Loss

Sequence Accuracy
Visualizations

Automatically generate

Confusion Matrix

ROC Curve

PR Curve

Class Distribution

Feature Importance

SHAP Summary Plot

Training Curves

Save all figures inside

backend/results/
Logging

During training

display

Training Isolation Forest...

Completed

Training Autoencoder...

Completed

Training LSTM...

Completed

Training XGBoost...

Completed

Saving Models...

Done

Generating Evaluation...

Done
Phase 2 Deliverables

By the end of Phase 2, the project must:

Build a complete feature engineering pipeline.
Learn normal behavior using Isolation Forest and an Autoencoder.
Learn temporal behavior using an LSTM.
Classify attacks using XGBoost.
Generate dynamic risk scores.
Explain predictions with SHAP and human-readable reasons.
Save trained models for inference.
Produce evaluation metrics and visualizations for the final report.
Expose a single prediction pipeline that transforms raw events into actionable security alerts.
Cursor Development Rules
Keep the code modular but avoid unnecessary abstraction.
Use one file per major ML responsibility.
Write clean, well-commented Python with type hints.
Save all trained models so retraining is optional.
Make every stage independently testable.
Prefer readable code over clever optimizations.
Ensure every prediction includes a classification, confidence, risk score, and explanation.
Structure the pipeline so additional attack types can be added later with minimal changes.