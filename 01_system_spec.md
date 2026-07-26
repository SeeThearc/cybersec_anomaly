That's a good decision. Simple architecture wins hackathons. Judges care about functionality, clean design, and a working demo more than having 200 files.

I would keep it around 35–45 files total instead of 150+.

MASTER PROMPT - PART 1
AI-Driven User & Entity Behavior Analytics (UEBA) System
Project Overview

I want you to build a production-quality but hackathon-friendly AI-powered User and Entity Behavior Analytics (UEBA) platform.

The project should detect abnormal user behavior from authentication logs, access logs, and device activities.

The goal is NOT to build a simple anomaly detector.

The goal is to build a complete AI security monitoring platform capable of

generating synthetic enterprise logs
simulating cyber attacks
learning normal user behaviour
detecting anomalies
classifying attacks
providing explanations
exposing APIs
displaying results on a dashboard

The architecture must remain simple, modular and clean.

Avoid unnecessary abstraction.

Avoid creating excessive folders.

Every module should have one responsibility.

Tech Stack

Frontend

React
Vite
TailwindCSS
Axios
Recharts

Backend

FastAPI
SQLAlchemy
PostgreSQL

Machine Learning

Pandas
NumPy
Scikit-learn
TensorFlow/Keras
XGBoost
SHAP

Others

Faker
Uvicorn
Pydantic
Folder Structure

Keep the project minimal.

UEBA-System/

backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── utils.py
│   │
│   ├── api.py
│   │
│   ├── ml/
│   │      data_generator.py
│   │      feature_engineering.py
│   │      train.py
│   │      predict.py
│   │
│   └── services/
│          profiler.py
│          attack_simulator.py
│
├── data/
│
├── trained_models/
│
├── requirements.txt
│
└── run.py


frontend/

src/

components/

pages/

services/

App.jsx

main.jsx

Don't introduce unnecessary services, repositories, managers, controllers, helpers, factories, or design patterns.

Database

Use PostgreSQL.

Create only these tables.

Users
id

name

department

role

country

joining_date
Devices
id

user_id

device_name

device_type

operating_system

browser

fingerprint
Events

This is the most important table.

id

user_id

timestamp

country

ip_address

device_id

resource

action

authentication_method

session_duration

login_status

failed_attempts

bytes_transferred

command_sequence

label

label contains

Normal

BruteForce

CredentialStuffing

ImpossibleTravel

DeviceSpoofing

LateralMovement

LowSlowExfiltration

InsiderDrift
Alerts
id

user_id

risk_score

attack_type

prediction

explanation

created_at
Synthetic Data Generator

Do NOT randomly generate logs.

Generate realistic enterprise behaviour.

Step 1

Generate employees.

Example

1000 Users

Each user belongs to

HR

Finance

Engineering

Sales

IT

Security

Each employee gets

Work Hours

Country

Known Devices

Average Login Time

Average Session

Frequently Accessed Resources

Authentication Method

Average Downloads

Average Uploads

This is the user's behavioural profile.

Step 2

Generate Normal Behaviour

Example

9:10 Login

↓

Email

↓

Jira

↓

GitHub

↓

Logout

Another employee

10:20 Login

↓

Payroll

↓

Finance Portal

↓

Logout

Generate around

50-200 events

per employee

This creates the baseline.

Step 3

Attack Simulation Engine

Instead of modifying random values,

simulate realistic cyber attacks.

Attack 1

Brute Force

Generate

Failed Login

Failed Login

Failed Login

Failed Login

Login Success

Properties

High Login Frequency

High Failure Count

Same IP

Small Time Difference

Store label

BruteForce
Attack 2

Impossible Travel

Example

09:00

India

↓

09:30

Germany

Automatically calculate

Distance

Travel Time

Travel Speed

Mark

ImpossibleTravel
Attack 3

Credential Stuffing

Generate

One IP

↓

Many Users

↓

Multiple Failures

Example

IP A

tries

User1

User2

User3

User4

User5

Store

CredentialStuffing
Attack 4

Device Spoofing

Normal

Windows

Chrome

Dell Laptop

Attack

Linux

Firefox

Unknown Device

Different Fingerprint

Store

DeviceSpoofing
Attack 5

Lateral Movement

Generate sequences like

Email

↓

HR Server

↓

Payroll

↓

Database

↓

Admin Console

instead of

Email

↓

GitHub

↓

Logout

Label

LateralMovement
Attack 6

Low-and-Slow Exfiltration

Instead of

100 GB

Generate

Day1

5 MB

Day2

7 MB

Day3

8 MB

Day4

10 MB

Day5

15 MB

Gradually increasing.

Store

LowSlowExfiltration
Attack 7

Insider Drift

Employee changes role.

Week 1

Email

GitHub

Week 2

Email

GitHub

Payroll

Week 3

Email

GitHub

Payroll

Admin Portal

Gradually changing behaviour.

Store

InsiderDrift
Dataset Split

Automatically create

train.csv

validation.csv

test.csv

Store inside

backend/data/
Data Distribution

Maintain class imbalance similar to real enterprises.

Normal

90%

Brute Force

2%

Credential Stuffing

2%

Impossible Travel

1%

Device Spoofing

1%

Lateral Movement

1%

Low-and-Slow Exfiltration

2%

Insider Drift

1%

Do NOT generate balanced datasets.

Data Validation

Before saving

Validate

No missing timestamps
Valid countries
Correct user IDs
Existing devices
Positive session duration
Valid login status
Correct labels

Reject corrupted rows.

Backend APIs (Phase 1 Only)

Implement only these APIs for now.

POST

/generate-data

Generates users, devices, events and attacks.
GET

/events

Returns generated logs.
GET

/users

Returns user profiles.

GET

/statistics

Returns

Total Users

Total Events

Attack Counts

Normal Events

Department Distribution
Phase 1 Deliverables

At the end of Phase 1 the project must be able to

✅ Generate realistic enterprise users.

✅ Generate behaviour profiles.

✅ Generate normal activity.

✅ Simulate all required attacks.

✅ Store everything inside PostgreSQL.

✅ Export train, validation and test datasets.

✅ Expose APIs to retrieve data and statistics.

Important Development Rules
Keep the architecture simple and readable.
Write clean, modular code with comments where necessary.
Use type hints in Python.
Avoid over-engineering and unnecessary design patterns.
Make every module independently testable.
Generate realistic synthetic data instead of random noise.