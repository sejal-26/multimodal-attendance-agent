import os
import cv2
import json
import asyncio
from typing import List
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from core.database import init_db
from core.face_detection import FaceDetector
from core.camera_service import CameraService
from core.face_recognition import FaceRecognizer, PresenceAttendanceTracker
from core.audio_analysis import AudioAnalyzer
from core.multimodal_agent import MultimodalAgent
from core.ai_insights import InsightGenerator
from core.ai_suggestions import AISuggestionsEngine
from core.recommendations_engine import RecommendationsEngine
from core.teacher_profiles import TeacherProfileService
from core.analytics_service import AnalyticsService

load_dotenv()

# Initialize Database
init_db()

app = FastAPI(
    title="Multimodal Attendance & Engagement Agent",
    description="Privacy-preserving classroom intelligence system integrating CV, Audio & AI Agent reasoning.",
    version="1.0.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Services
face_detector = FaceDetector()
camera_service = CameraService(camera_id=0)
camera_service.start()

face_recognizer = FaceRecognizer()
attendance_tracker = PresenceAttendanceTracker(threshold_seconds=10.0)
audio_analyzer = AudioAnalyzer()
multimodal_agent = MultimodalAgent(session_id=1)
insight_generator = InsightGenerator()
suggestions_engine = AISuggestionsEngine()
recommendations_engine = RecommendationsEngine()
teacher_service = TeacherProfileService()
analytics_service = AnalyticsService()

# Serve static frontend files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Multimodal Attendance & Engagement Agent Backend Running</h1>")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "camera_active": camera_service.is_running
    }

@app.get("/api/session/status")
async def get_session_status():
    """Returns current fused multimodal session metrics and participants."""
    frame = camera_service.get_frame()
    detections = []
    if frame is not None:
        raw_faces = face_detector.process_frame(frame)
        for face in raw_faces:
            s_id, s_name, _ = face_recognizer.recognize(frame, face["bbox"])
            face["student_id"] = s_id
            face["student_name"] = s_name
            detections.append(face)

    # Update attendance tracking
    attendance_summary = attendance_tracker.update_presence(detections)

    # Fuse multimodal signals
    fused_state = multimodal_agent.fuse_and_score(detections, attendance_summary)
    
    # Generate real-time recommendations
    recs = recommendations_engine.generate_realtime_recommendations(fused_state)
    fused_state["recommendations"] = recs

    # Generate AI insights
    fused_state["ai_insight"] = insight_generator.generate_classroom_insight(fused_state)
    fused_state["teaching_suggestions"] = suggestions_engine.generate_suggestions(fused_state)
    fused_state["attendance"] = attendance_summary

    return fused_state

@app.get("/api/attendance")
async def get_attendance():
    """Returns structured presence-based attendance log."""
    return attendance_tracker.get_attendance_summary()

@app.get("/api/teacher-profile")
async def get_teacher_profile(teacher_id: str = "T101"):
    """Returns teacher effectiveness profile matching Teacher Central dashboard."""
    return teacher_service.get_profile(teacher_id)

@app.get("/api/analytics")
async def get_analytics(session_id: int = 1):
    """Returns session attention trend and emotion distribution over time."""
    return analytics_service.get_session_trends(session_id)

@app.get("/api/analytics/export-csv")
async def export_analytics_csv(session_id: int = 1):
    """CSV export for classroom session analytics report."""
    csv_data = analytics_service.export_csv(session_id)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=session_{session_id}_report.csv"}
    )

def generate_video_frames():
    """Generator for MJPEG video stream with bounding boxes and HUD labels."""
    while True:
        frame = camera_service.get_frame()
        if frame is None:
            time.sleep(0.05)
            continue

        raw_faces = face_detector.process_frame(frame)
        for face in raw_faces:
            x, y, w, h = face["bbox"]
            s_id, s_name, _ = face_recognizer.recognize(frame, (x, y, w, h))
            orientation = face.get("orientation", "center")
            att_score = 88 if orientation == "center" else 55

            # Bounding box color based on attention
            color = (0, 220, 100) if att_score >= 70 else (0, 140, 255) # Green / Amber
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # Label banner
            label = f"{s_name} | {att_score}%"
            cv2.rectangle(frame, (x, y - 24), (x + w, y), color, -1)
            cv2.putText(frame, label, (x + 6, y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        if not ret:
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        asyncio.run(asyncio.sleep(0.04))

@app.get("/api/video-feed")
async def video_feed():
    """MJPEG stream for live video canvas."""
    return StreamingResponse(
        generate_video_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    """WebSocket endpoint for streaming browser audio analysis (Activity 3.1 & 3.2)."""
    await websocket.accept()
    try:
        while True:
            # Receive audio chunk (bytes or json)
            message = await websocket.receive()
            if "bytes" in message and message["bytes"]:
                metrics = audio_analyzer.analyze_audio_chunk(message["bytes"])
                multimodal_agent.update_audio(metrics)
                await websocket.send_json(metrics)
            elif "text" in message and message["text"]:
                data = json.loads(message["text"])
                if "audio_level" in data:
                    # Browser computed audio level
                    db = float(data.get("audio_level", -28.0))
                    metrics = {
                        "rms": 0.02,
                        "decibels": db,
                        "is_speech": db > -30.0,
                        "speech_ratio": 0.3 if db > -30.0 else 0.05,
                        "activity_pattern": "lecture" if db > -30.0 else "quiet"
                    }
                    multimodal_agent.update_audio(metrics)
                    await websocket.send_json(metrics)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket audio exception: {e}")
