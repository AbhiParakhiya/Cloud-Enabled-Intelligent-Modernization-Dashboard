# Architecture Overview

## Business Context
The client required modernization of a legacy Java-based batch processing system. The goal was to introduce real-time decisioning, predictive analytics, and a modern web dashboard without rewriting the core legacy logic immediately.

## Solution Architecture

### 1. Legacy Layer (Existing)
- **Component**: Java Batch Processor
- **Function**: Processes nightly transactions from `legacy_system.db`.
- **Status**: Retained and integrated.

### 2. Data Intelligence Layer (New)
- **Component**: Python ETL & Analytics Engine
- **Function**: 
  - Extracts data from SQLite.
  - Cleans and engineers features (e.g., `account_age`, `tx_hour`).
  - Performs Exploratory Data Analysis (EDA).

### 3. Machine Learning Core (New)
- **Models**:
  - **Logistic Regression**: Predicts High Value/Risk transactions.
  - **Random Forest**: Backup classifier for performance comparison.
  - **K-Means**: Segments customers into clusters based on behavior.
- **Artifacts**: Serialized `.pkl` models.

### 4. API Layer (New)
- **Tech**: FastAPI
- **Function**: Exposes ML models as REST endpoints (`/predict/risk`, `/predict/segment`).
- **Integration**: Allows the legacy Java app (or other consumers) to request real-time scoring.

### 5. Presentation Layer (New)
- **Tech**: Streamlit
- **Function**: Interactive dashboard for stakeholders to view KPIs, EDA plots, and test model inference.

### 6. Infrastructure (New)
- **Containerization**: Docker & Docker Compose.
- **Cloud Readiness**: Ready for deployment on AWS ECS or Azure Container Instances.

## Tech Stack
- **Languages**: Java (Legacy), Python (Modernization)
- **Database**: SQLite (Simulated SQL Backend)
- **ML/DS**: Pandas, Scikit-learn, Matplotlib, Seaborn
- **Web**: FastAPI, Streamlit
- **DevOps**: Docker
