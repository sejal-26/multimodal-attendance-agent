import time
from datetime import datetime
from .database import SessionLocal, PersonMetric

class MultimodalAgent:
    """
    Milestone 4: Activity 4.1 Multimodal Signal Fusion & Activity 4.2 Engagement Scoring Logic
    Fuses vision metrics (face detection, orientation, sustained presence)
    with audio metrics (noise level, speech ratio, acoustic state).
    """
    def __init__(self, session_id=1):
        self.session_id = session_id
        self.last_audio_metrics = {
            "rms": 0.02,
            "decibels": -28.0,
            "is_speech": False,
            "speech_ratio": 0.1,
            "activity_pattern": "lecture"
        }

    def update_audio(self, audio_metrics: dict):
        if audio_metrics:
            self.last_audio_metrics.update(audio_metrics)

    def fuse_and_score(self, visual_detections: list, attendance_records: list = None):
        """
        Fuses visual detections and current audio state to compute individual & session engagement.
        """
        now = datetime.utcnow()
        db = SessionLocal()

        people_status = []
        audio_db = self.last_audio_metrics.get("decibels", -28.0)
        is_speech = self.last_audio_metrics.get("is_speech", False)
        sound_pattern = self.last_audio_metrics.get("activity_pattern", "normal")

        total_attention = 0.0

        for idx, det in enumerate(visual_detections):
            s_id = det.get("student_id", f"P{idx+1}")
            s_name = det.get("student_name", f"Student {idx+1}")
            orientation = det.get("orientation", "center")

            # Base visual attention score (0 - 100)
            if orientation == "center":
                base_visual = 88.0
                emotion = "attentive"
            elif orientation in ["turned_left", "turned_right"]:
                base_visual = 55.0
                emotion = "distracted"
            else:
                base_visual = 70.0
                emotion = "neutral"

            # Audio modulation: in interactive/speech contexts, looking around is normal
            if is_speech and sound_pattern == "active student discussion":
                engagement_score = min(100.0, base_visual + 8.0)
            elif audio_db > -12.0: # excessive noise
                engagement_score = max(30.0, base_visual - 10.0)
            else:
                engagement_score = base_visual

            total_attention += engagement_score

            person_info = {
                "id": s_id,
                "name": s_name,
                "bbox": det.get("bbox", (0, 0, 100, 100)),
                "attention": round(engagement_score, 1),
                "emotion": emotion,
                "orientation": orientation
            }
            people_status.append(person_info)

            # Record metric to DB
            try:
                metric = PersonMetric(
                    session_id=self.session_id,
                    student_id=s_id,
                    student_name=s_name,
                    timestamp=now,
                    attention_score=engagement_score,
                    emotion=emotion,
                    head_pose=orientation,
                    noise_level=audio_db
                )
                db.add(metric)
            except Exception:
                pass

        try:
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

        avg_attention = round(total_attention / len(people_status), 1) if people_status else 80.0

        return {
            "session_id": self.session_id,
            "timestamp": now.strftime("%H:%M:%S"),
            "participant_count": len(people_status),
            "avg_attention": avg_attention,
            "people": people_status,
            "audio": self.last_audio_metrics,
            "noise_level": audio_db,
            "activity_pattern": sound_pattern
        }
