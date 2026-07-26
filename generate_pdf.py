import os
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Preformatted
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError:
    print("Please install reportlab first: pip install reportlab")
    exit(1)

def create_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10
    )
    p_style = ParagraphStyle(
        'CustomP',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leading=16
    )
    li_style = ParagraphStyle(
        'CustomLI',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        leftIndent=15
    )

    Story = []

    # Title
    Story.append(Paragraph("Project Report: User & Entity Behavior Analytics (UEBA)", title_style))

    # 1. Overview
    Story.append(Paragraph("1. Overview", h2_style))
    Story.append(Paragraph("I developed a comprehensive User and Entity Behavior Analytics (UEBA) platform designed to detect complex cyber threats like insider drift, compromised credentials, and lateral network movement. Instead of relying on static, rules-based thresholds that generate too many false positives, this system uses machine learning to learn what 'normal' looks like for every individual employee and flags statistical deviations in real-time.", p_style))

    # 2. System Architecture
    Story.append(Paragraph("2. System Architecture", h2_style))
    Story.append(Paragraph("The platform is built on a modern, decoupled architecture:", p_style))
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=9,
        leading=12,
        leftIndent=20,
        spaceAfter=10,
        fontName='Courier'
    )
    
    diagram = """
    [ CLIENT TIER ]                                    [ DATA TIER ]
    +-----------------------------------+              +-----------------------------------+
    | React (Vite) Frontend             |              | PostgreSQL Database               |
    |  - Dashboards & Telemetry Charts  |              |  - Users & Entity Profiles        |
    |  - Recharts / Tailwind CSS        |              |  - Enterprise Event Logs          |
    |  - Axios API Client               |              |  - Security Alerts & SHAP Scores  |
    +-----------------------------------+              +-----------------------------------+
                      ||                                                ||
         (HTTP POST / GET Polling)                               (SQLAlchemy ORM)
                      ||                                                ||
    [ APPLICATION TIER ] ===================================================================
    | +----------------------------------------------------------------------------------+ |
    | | FastAPI Backend (Async Uvicorn Server)                                           | |
    | |  - Pydantic Validation & Security Router                                         | |
    | +----------------------------------------------------------------------------------+ |
    |         ||                                                             ||            |
    |         \/                                                             \/            |
    | +--------------------------------------------------+   +---------------------------+ |
    | | Machine Learning Detection Pipeline              |   | AI Security Copilot       | |
    | |  1. Feature Eng: Pandas (Time-series / Lags)     |   |  - LangChain LCEL Routing | |
    | |  2. Behavior Profiler: Isolation Forest        |   |  - Prompt Templates       | |
    | |  3. Sequence Profiler: LSTM (TensorFlow/Keras)   |   |  - Gemini 2.5 Flash API   | |
    | |  4. Threat Classifier: XGBoost                   |   |                           | |
    | |  5. Explainability: SHAP (Feature Importance)    |   |                           | |
    | +--------------------------------------------------+   +---------------------------+ |
    ========================================================================================
    """
    
    Story.append(Preformatted(diagram, code_style))
    Story.append(Paragraph("<b>Why I chose this architecture:</b> I designed this decoupled, asynchronous flow because it guarantees that the heavy machine learning inference tasks never block the high-frequency telemetry polling required by the real-time SOC dashboard.", p_style))

    
    arch_items = [
        ListItem(Paragraph("<b>Backend:</b> A high-performance Python backend using FastAPI and SQLAlchemy.", li_style)),
        ListItem(Paragraph("<b>Database:</b> PostgreSQL for storing enterprise telemetry, user profiles, device fingerprints, and security alerts.", li_style)),
        ListItem(Paragraph("<b>Frontend:</b> A React/Vite dashboard featuring real-time polling, Recharts for data visualization, and a complete UI for managing alerts, viewing user directories, and configuring system settings.", li_style)),
        ListItem(Paragraph("<b>AI Copilot:</b> I integrated a LangChain-powered LLM directly into the backend to translate raw, complex mathematical alerts into plain English summaries for SOC analysts.", li_style))
    ]
    Story.append(ListFlowable(arch_items, bulletType='bullet', spaceAfter=12))

    # 3. ML Pipeline
    Story.append(Paragraph("3. Machine Learning Pipeline", h2_style))
    Story.append(Paragraph("The core of the project is the ML pipeline, which I built to process data in stages:", p_style))
    
    ml_items = [
        ListItem(Paragraph("<b>Realistic Data Simulation:</b> Since getting real enterprise attack data is difficult, I built a custom data generator. It uses log-normal statistical distributions to simulate realistic human behavior (e.g., heavily skewed data transfer sizes and varied session durations) across 100,000+ events.", li_style)),
        ListItem(Paragraph("<b>Feature Engineering:</b> The pipeline uses Pandas to extract time-series features. It handles timezone alignments and calculates rolling averages, such as the time elapsed since a user's last login.", li_style)),
        ListItem(Paragraph("<b>Behavior Profiling:</b> I trained an Isolation Forest algorithm to establish a unique behavioral baseline for each user based on their specific department and historical access patterns.", li_style)),
        ListItem(Paragraph("<b>Sequence Detection (LSTM):</b> To catch attackers pivoting through the network, I implemented an LSTM neural network. It tracks the sequence of resources a user accesses and spikes an anomaly score if they make an unpredictable hop (Lateral Movement).", li_style)),
        ListItem(Paragraph("<b>Threat Classification (XGBoost):</b> An XGBoost classifier takes the anomaly scores from the previous models and categorizes the threat into one of 7 specific attack vectors (e.g., Brute Force, Impossible Travel, Low & Slow Exfiltration).", li_style)),
        ListItem(Paragraph("<b>Explainability:</b> I integrated SHAP (SHapley Additive exPlanations) so the system doesn't act as a black box. Every alert explicitly lists the top features that triggered the model.", li_style))
    ]
    Story.append(ListFlowable(ml_items, bulletType='bullet', spaceAfter=12))

    # 4. Key Innovations
    Story.append(Paragraph("4. Key Innovations (Novelty)", h2_style))
    Story.append(Paragraph("What makes this UEBA platform truly novel is how it solves the 'Black Box Problem' and the 'False Positive Fatigue' that plague traditional cybersecurity systems:", p_style))
    
    novel_items = [
        ListItem(Paragraph("<b>Dynamic Human Baselines (Not Static Rules):</b> Traditional SIEMs rely on hardcoded thresholds that attackers easily bypass. Our Isolation Forest learns the mathematical 'fingerprint' of how every individual employee normally behaves based on their specific department, flagging deviations even if no static rule was broken.", li_style)),
        ListItem(Paragraph("<b>Explainable, Sequence-Aware Ensemble AI:</b> We use a stacked ML architecture (Isolation Forest + LSTM + XGBoost) to detect temporal sequence anomalies like Lateral Movement. We then solve the ML 'Black Box' problem by extracting mathematical feature importance via SHAP and piping it directly into a LangChain GenAI Copilot, automatically translating complex ML mathematics into plain-English threat intelligence.", li_style))
    ]
    Story.append(ListFlowable(novel_items, bulletType='bullet', spaceAfter=12))

    # 5. Results
    Story.append(Paragraph("5. Evaluation & Results", h2_style))
    Story.append(Paragraph("The system successfully met all initial evaluation criteria:", p_style))
    
    res_items = [
        ListItem(Paragraph("<b>Performance:</b> End-to-end inference (pulling DB history -> Feature Engineering -> LSTM -> XGBoost -> SHAP) executes in under 500ms.", li_style)),
        ListItem(Paragraph("<b>Accuracy:</b> By forcing the prediction API to dynamically pull the user's historical context from the database, the model accurately classifies incoming single-event payloads without needing any hardcoded logic or fake overrides.", li_style)),
        ListItem(Paragraph("<b>Resilience:</b> The pipeline gracefully handles cold-starts (new users with no history) and resolves mixed-timezone issues natively.", li_style))
    ]
    Story.append(ListFlowable(res_items, bulletType='bullet', spaceAfter=12))

    # 6. Future
    Story.append(Paragraph("6. Future Considerations", h2_style))
    Story.append(Paragraph("To scale this proof-of-concept into a production environment processing millions of daily events, I would look at implementing:", p_style))
    
    fut_items = [
        ListItem(Paragraph("<b>Streaming Ingestion:</b> Replacing the synchronous REST API log ingestion with a message broker like Apache Kafka.", li_style)),
        ListItem(Paragraph("<b>Continuous Learning:</b> Setting up an Airflow DAG to automatically retrain the Isolation Forest models every 30 days to account for natural shifts in company behavior (concept drift).", li_style))
    ]
    Story.append(ListFlowable(fut_items, bulletType='bullet', spaceAfter=12))

    doc.build(Story)
    print(f"Successfully generated PDF at {output_path}")

if __name__ == "__main__":
    output_file = os.path.join(os.getcwd(), "Project_Final_Report.pdf")
    create_pdf(output_file)
