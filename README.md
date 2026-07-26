# 🛡️ AI-Driven UEBA Security Platform

An advanced User and Entity Behavior Analytics (UEBA) platform that leverages Machine Learning and Generative AI to detect, visualize, and explain insider threats and compromised accounts in real-time.

---

## 🏗️ Architecture Diagram

```mermaid
graph TD
    subaxis
        UI[React Dashboard]
        Copilot[AI Security Copilot]
    end
    
    subaxis
        API[FastAPI Backend]
        DB[(PostgreSQL)]
    end

    subaxis ML Pipeline
        FE[Feature Engineering]
        BP[Isolation Forest + Autoencoder]
        SP[LSTM Sequence Model]
        XGB[XGBoost Classifier]
        SHAP[SHAP Explainer]
    end

    UI <--> |REST API| API
    Copilot <--> |REST API| API
    
    API <--> |CRUD| DB
    API --> |Raw Event| FE
    
    FE --> BP
    FE --> SP
    
    BP --> XGB
    SP --> XGB
    FE --> XGB
    
    XGB --> |Prediction| SHAP
    SHAP --> |Risk Score & Explanation| API
```

---

## 🚀 Features
- **Real-Time ML Pipeline:** Cascading models (Isolation Forest -> Autoencoder -> LSTM -> XGBoost) to detect geographic anomalies, baseline deviations, and complex sequence attacks.
- **Dynamic Threat Visualization:** A React frontend using Vite, TailwindCSS, and Recharts to render real-time ROC curves, SHAP importance, and a live alert timeline.
- **AI Security Copilot:** Integrated with Google Gemini 2.5 to provide natural language explanations, context-aware summaries, and immediate mitigation steps for triggered alerts.
- **Explainable AI (XAI):** Uses SHAP to crack open the "black box" of the ML models, telling analysts exactly *why* a user was flagged.

---

## 🛠️ Installation Guide

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL Server

### 1. Database Setup
Ensure PostgreSQL is running locally and create a database (e.g., `ueba_db`).
Update your backend environment variables with your DB credentials.

### 2. Backend Setup (FastAPI & ML)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# Configure Environment
cp .env.example .env 
# (Add your DATABASE_URL and GEMINI_API_KEY to .env)

# Generate Synthetic Data & Train ML Models
python app/ml/data_generator.py
python train.py

# Seed the Dashboard with Demo Alerts
python seed_alerts.py
or use swagger - \docs for alerting via json request to predict

# Start the API Server
uvicorn app.main:app --reload
```

### 3. Frontend Setup (React & Vite)
```bash
cd frontend
npm install

# Start the Development Server
npm run dev
```

---

## 📖 Usage Guide

1. **Dashboard Overview:** Open `http://localhost:5173`. Watch the real-time counters, risk gauges, and event timelines auto-refresh as data enters the system.
2. **Analytics Deep Dive:** Navigate to the `/analytics` tab to inspect model performance (ROC/PR Curves, Confusion Matrices, and SHAP feature importance).
3. **AI Copilot:** Navigate to the `/copilot` tab. Ask the AI questions like *"Why was User 1 flagged?"* or *"What are my mitigation steps?"* The Copilot dynamically pulls the latest telemetry from the database to answer.
4. **Trigger Live Inferences:** Use the Swagger UI at `http://localhost:8000/docs` to POST an event to the `/predict` endpoint. Watch the ML pipeline catch anomalies (like Impossible Travel or Credential Stuffing) and instantly broadcast them to the React UI.

---

## 📡 API Documentation

A full interactive Swagger UI is available at `http://localhost:8000/docs`.

### Key Endpoints:
- `POST /predict`: Submit a raw JSON event. Returns the model's prediction, confidence, SHAP explanation, and overall risk score.
- `GET /statistics`: Returns high-level database aggregations (Total Events, Active Threats, High Risk Users) for the dashboard.
- `GET /analytics`: Returns deep ML metrics (ROC, Confusion Matrix, Attack Distributions) for charting.
- `GET /alerts`: Fetches the latest security alerts, ordered by timestamp descending.
- `POST /copilot`: Send a query to the integrated Gemini SOC assistant.

---

## 🧪 Testing

The platform features automated testing for both stacks.

**Backend (pytest):**
```bash
cd backend
python -m pytest
```

**Frontend (vitest):**
```bash
cd frontend
npm run test
```

---

## 🔮 Future Scope
- **Streaming Ingestion:** Replace the REST API bottleneck with Apache Kafka or RabbitMQ for high-throughput, asynchronous log processing.
- **Graph Neural Networks (GNNs):** Map user-to-device-to-resource interactions in a graph database (Neo4j) to better detect Lateral Movement paths.
- **Automated Mitigation (SOAR):** Connect the Risk Engine directly to Active Directory or Okta APIs to instantly suspend accounts when `risk_score > 90`, rather than just alerting the dashboard.
