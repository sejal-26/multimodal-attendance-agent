import os

class InsightGenerator:
    """
    Milestone 4: Multimodal Agent Implementation
    Activity 4.3: AI-Driven Classroom Insights
    Generates actionable educational insights using Groq LLM (with robust fallback).
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key and self.api_key != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"InsightGenerator: Could not initialize Groq client: {e}")

    def generate_classroom_insight(self, session_data: dict) -> dict:
        """
        Generates context-aware insight based on fused vision and audio metrics.
        """
        avg_att = session_data.get("avg_attention", 82.0)
        participants = session_data.get("participant_count", 2)
        noise = session_data.get("noise_level", -28.0)
        sound_pattern = session_data.get("activity_pattern", "normal classroom lecture")

        prompt = (
            f"Classroom Status: Average Attention={avg_att:.1f}%, Active Participants={participants}, "
            f"Noise Level={noise:.1f} dB, Audio State='{sound_pattern}'. "
            f"Provide a 1-sentence diagnostic insight and 1-sentence teaching recommendation."
        )

        if self.client:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert educational AI assistant. Provide brief, professional, "
                                "and actionable insights for classroom engagement. Keep it under 2 sentences."
                            )
                        },
                        {"role": "user", "content": prompt},
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.5,
                    max_tokens=150,
                )
                response_text = chat_completion.choices[0].message.content.strip()
                return {
                    "insight": response_text,
                    "status": "healthy" if avg_att >= 70 else "needs_attention",
                    "source": "AI (Groq/Llama-3)"
                }
            except Exception as e:
                print(f"InsightGenerator Groq API error: {e}. Using rule-based fallback.")

        # Fallback rule-based insight
        return self._fallback_insight(session_data)

    def _fallback_insight(self, session_data: dict) -> dict:
        avg_att = session_data.get("avg_attention", 82.0)
        sound_pattern = session_data.get("activity_pattern", "normal")

        if avg_att >= 85:
            return {
                "insight": "High classroom engagement detected. Active visual attention indicates optimal pacing.",
                "status": "optimal",
                "source": "Multimodal Rule Engine"
            }
        elif avg_att >= 70:
            return {
                "insight": f"Classroom engagement is stable at {avg_att:.1f}%. Audio activity confirms focused listening.",
                "status": "stable",
                "source": "Multimodal Rule Engine"
            }
        elif avg_att >= 50:
            return {
                "insight": f"Noticeable attention dip ({avg_att:.1f}%). Suggest asking a discussion question or quick quiz.",
                "status": "warning",
                "source": "Multimodal Rule Engine"
            }
        else:
            return {
                "insight": "Multiple students exhibiting disengagement. Recommend taking a 2-minute break or change of modality.",
                "status": "alert",
                "source": "Multimodal Rule Engine"
            }
