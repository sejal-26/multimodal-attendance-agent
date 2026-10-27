# 🎓 Multimodal Attendance & Engagement Agent

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Haar%20Cascade-5C3EE8.svg)](https://opencv.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-powered, privacy-preserving classroom intelligence system that integrates **Computer Vision**, **Audio Signal Processing**, and **Agent-Based Reasoning** to automatically track attendance based on sustained presence, analyze multidimensional engagement trends, generate context-aware teaching suggestions, and provide reflective session analytics for educators.

---

## 📌 Table of Contents
1. [Project Overview & Scenarios](#-project-overview--scenarios)
2. [Key Features & System Capabilities](#-key-features--system-capabilities)
3. [System Architecture](#-system-architecture)
4. [Project Structure](#-project-structure)
5. [Milestone & Activity Implementation](#-milestone--activity-implementation)
6. [Running the Application](#-running-the-application)
7. [API Endpoints](#-api-endpoints)

---

## 🎯 Project Overview & Scenarios

In traditional educational and professional training environments, attendance tracking remains largely manual or limited to single-frame biometric scans that fail to capture meaningful engagement and participation context.

The **Multimodal Attendance & Engagement Agent** solves this through three primary scenarios:

### 1. Scenario 1: Automated Attendance Tracking
Processes live or recorded classroom video feeds to detect and track participants. Instead of error-prone single-frame scans, attendance is confirmed only after **sustained presence** exceeding a predefined time threshold (e.g. 15s). Automated, timestamped attendance logs are generated without interrupting instructional flow.

### 2. Scenario 2: Engagement and Session Dynamics Analysis
Continuously analyzes behavioral signals including head pose / face orientation, spatial stability, inactivity duration, and classroom acoustic energy (decibels and speech activity). These multimodal signals are fused into interpretable engagement scores over time.

### 3. Scenario 3: AI-Driven Teaching Suggestions
Using fused multimodal data, an assistive AI agent generates non-prescriptive, actionable pedagogical recommendations (e.g., suggesting interactive polls when group attention drops, or pacing adjustments during high noise intervals).

---

## ✨ Key Features & System Capabilities

- Automated attendance tracking based on sustained participant presence.
- Face detection using OpenCV.
- Audio signal analysis, including acoustic energy and speech activity.
- Multimodal engagement scoring using vision and audio signals.
- AI-driven classroom insights and teaching suggestions.
- Teacher Central dashboard with session trends and recommendations.
- Interactive analytics and session reports.
- Attendance and analytics export in CSV and PDF formats.
- FastAPI-based web dashboard with real-time updates.
- Optional Streamlit dashboard.

## 🏗️ System Architecture

```
                       ┌──────────────────────────────┐
                       │  Classroom Video & Audio     │
                       └──────────────┬───────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
   ┌───────────────────────┐                       ┌───────────────────────┐
   │     Vision Module     │                       │     Audio Module      │
   │  - Face Detection     │                       │  - Signal Extraction  │
   │  - Spatial Tracking   │                       │  - RMS & Decibel (dB) │
   │  - Presence Duration  │                       │  - Speech/Silence VAD │
   └──────────┬────────────┘                       └──────────┬────────────┘
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      ▼
                       ┌──────────────────────────────┐
                       │   Multimodal Fusion Agent    │
                       │  - Timestamp Synchronization │
                       │  - Engagement Scoring Logic  │
                       │  - Threshold Evaluation      │
                       └──────────────┬───────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
   ┌───────────────────────┐                       ┌───────────────────────┐
   │ Recommendation Engine │                       │  Analytics & Profiles │
   │  - Real-Time Alerts   │                       │  - Teacher Central    │
   │  - Groq / LLM Insights│                       │  - Session Timelines  │
   │  - Teaching Advice    │                       │  - CSV/PDF Export     │
   └──────────┬────────────┘                       └──────────┬────────────┘
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      ▼
                       ┌──────────────────────────────┐
                       │     User Interface Layer     │
                       │  - FastAPI Web Dashboard     │
                       │  - Streamlit Dashboard (6.2) │
                       └──────────────────────────────┘
```

---

## 📁 Project Structure

```
multimodal-attendance-agent/
│
├── backend/
│   ├── requirements.txt            # Python dependencies
│   ├── main.py                     # FastAPI server & WebSocket streaming
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py             # SQLite database models & session management
│   │   ├── camera_service.py       # Camera feed acquisition & fallback simulation
│   │   ├── face_detection.py       # OpenCV Haar Cascade face detection
│   │   ├── face_recognition.py     # Presence duration & attendance tracking logic
│   │   ├── audio_analysis.py       # Acoustic RMS, dB calculation & speech analysis
│   │   ├── multimodal_agent.py     # Multimodal signal fusion & engagement scoring
│   │   ├── ai_insights.py          # Groq / LLM diagnostic classroom insights
│   │   ├── ai_suggestions.py       # Actionable pedagogical teaching recommendations
│   │   ├── recommendations_engine.py # Rule-based real-time alerts
│   │   ├── teacher_profiles.py     # Teacher effectiveness profile & historical trends
│   │   └── analytics_service.py    # Time-series analytics aggregation & CSV export
│   └── static/
│       ├── index.html              # Modern dark-mode responsive web dashboard
│       ├── css/
│       │   └── style.css           # Styling matching SkillWallet dashboard UI
│       └── js/
│           ├── app.js              # Live metrics controller & Chart.js charts
│           └── audio_capture.js    # Browser Web Audio API & WebSocket stream
│
├── streamlit_app.py                # Optional Streamlit dashboard (Milestone 6 Activity 6.2)
├── run_server.py                   # Interactive unified application launcher
├── requirements.txt                # Root-level requirements for Cloud deployment
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore patterns
└── README.md                       # Comprehensive documentation
```

---


## 🖥️ Running the Application

### FastAPI Dashboard

Run the following command from the project root:

```bash
python run_server.py
```

Select option `1` to launch the FastAPI dashboard.

Open your browser and navigate to:

http://localhost:8000

### Streamlit Dashboard

Run:

```bash
streamlit run streamlit_app.py
```

Open your browser and navigate to:

http://localhost:8501


## 🚀 Milestone & Activity Implementation

| Milestone | Activity | Implementation File | Status |
| :--- | :--- | :--- | :--- |
| **Epic 1: Requirements & Setup** | 1.1 Create `requirements.txt`<br>1.2 Install virtual environment | `backend/requirements.txt`<br>`requirements.txt` | Complete |
| **Epic 2: Vision Module** | 2.1 Face detection & tracking<br>2.2 Presence-based attendance | `backend/core/face_detection.py`<br>`backend/core/face_recognition.py`<br>`backend/core/camera_service.py` | Complete |
| **Epic 3: Audio Module** | 3.1 Audio signal extraction<br>3.2 Noise & speech activity | `backend/core/audio_analysis.py`<br>`backend/static/js/audio_capture.js` | Complete |
| **Epic 4: Multimodal Agent** | 4.1 Signal fusion<br>4.2 Engagement scoring<br>4.3 LLM Classroom Insights | `backend/core/multimodal_agent.py`<br>`backend/core/ai_insights.py`<br>`backend/core/ai_suggestions.py` | Complete |
| **Epic 5: Analytics & Engine** | 5.1 Teaching suggestion logic<br>5.2 Student session analytics | `backend/core/recommendations_engine.py`<br>`backend/core/teacher_profiles.py`<br>`backend/core/analytics_service.py` | Complete |
| **Epic 6: Interface & Deployment** | 6.1 Run core application<br>6.2 Launch Streamlit dashboard<br>6.3 Output & edge case testing | `backend/main.py`<br>`streamlit_app.py`<br>`run_server.py` | Complete |


## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Main classroom dashboard interface |
| `GET` | `/api/session/status` | Current fused multimodal state, attention %, participants, AI insights |
| `GET` | `/api/attendance` | Structured presence-based attendance log |
| `GET` | `/api/teacher-profile` | Teacher effectiveness score, historical trends, recommendations |
| `GET` | `/api/analytics` | Session time series data (attention trend and emotion distribution) |
| `GET` | `/api/analytics/export-csv` | Downloads session attendance and metrics in CSV format |
| `GET` | `/api/video-feed` | Live MJPEG stream with bounding box HUD overlays |
| `WS` | `/ws/audio` | Real-time WebSocket audio streaming and analysis |

## 👩‍💻 Author

**Sejal Malviya**

- GitHub: [@sejal-26](https://github.com/sejal-26)
- Project: [Multimodal Attendance & Engagement Agent](https://github.com/sejal-26/multimodal-attendance-agent)

---

⭐ If you find this project interesting, feel free to star the repository!
## 📄 License
This project is licensed under the MIT License.
