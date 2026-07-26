# Goal Description
The objective is to completely regenerate the synthetic dataset with highly realistic, enterprise-grade data distributions, retrain all Machine Learning models from scratch on this new data, and verify that the end-to-end prediction pipeline flawlessly catches threats without any hardcoded overrides.

## Proposed Changes

### 1. Refine Data Generation (Realism Upgrades)
We will modify `app/ml/data_generator.py` and `app/services/attack_simulator.py` to make the data statistically indistinguishable from a real enterprise:
- **Data Volume Distributions:** Instead of uniform random distributions for `bytes_transferred` and `session_duration`, we will use **log-normal distributions**. (In real life, 95% of web requests are tiny JSON files <10KB, while 5% are massive data pulls. Uniform random numbers don't reflect this).
- **Time Spacing:** Brute force attacks will be sped up to occur milliseconds/seconds apart (simulating a real automated script) rather than minutes apart.
- **Geography:** IP addresses will be tied more strictly to geographic regions to make the "Impossible Travel" models work harder.

### 2. Generate New Dataset
- Run the data generator. This will truncate the current `users`, `events`, and `alerts` tables, generate ~100,000 highly realistic events, and output fresh `train.csv`, `validation.csv`, and `test.csv` files.

### 3. Retrain ML Models
- Run `train.py`. This will rebuild and save new versions of:
  - Feature Engineering Pipelines (Scalers, Encoders)
  - Behavior Profiler (Isolation Forest & Autoencoder)
  - Sequence Profiler (LSTM)
  - Attack Classifier (XGBoost)
  - Explainability Engine (SHAP)

## User Review Required

> [!WARNING]
> This will wipe your current database tables (Users, Events, Alerts) and overwrite your current ML models. 

Are you okay with proceeding with this complete wipe and retrain?

## Verification Plan
After training, I will use a custom script to inject several complex, single-event payloads into the `PredictionPipeline` (mimicking the API) and verify that the models accurately classify them based on the historical database context.
