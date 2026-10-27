import os

class AISuggestionsEngine:
    """
    Milestone 4: Activity 4.3 & Milestone 5: Activity 5.1
    Context-aware AI teaching suggestions based on multimodal session signals.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key and self.api_key != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"AISuggestionsEngine: Could not initialize Groq client: {e}")

    def generate_suggestions(self, session_data: dict):
        """
        Generates teaching suggestions tailored to current classroom dynamics.
        """
        avg_att = session_data.get("avg_attention", 75.0)
        noise = session_data.get("noise_level", -28.0)
        sound_pattern = session_data.get("activity_pattern", "lecture")

        prompt = (
            f"Classroom stats: Attention={avg_att:.1f}%, Sound pattern={sound_pattern}, Noise={noise:.1f} dB. "
            f"Provide 2 or 3 short, concrete bullet points for the teacher to optimize engagement right now."
        )

        if self.client:
            try:
                completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert AI teaching assistant. Provide direct, bulleted pedagogical advice."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=200
                )
                response = completion.choices[0].message.content
                return self._parse_response(response)
            except Exception as e:
                print(f"AI Suggestion Error: {e}")

        return self._fallback_suggestions(session_data)

    def _parse_response(self, text: str):
        lines = [line.strip("- *•0123456789. ") for line in text.splitlines() if line.strip()]
        return lines[:3] if lines else self._fallback_suggestions({})

    def _fallback_suggestions(self, session_data: dict):
        avg_att = session_data.get("avg_attention", 75.0)
        noise = session_data.get("noise_level", -28.0)

        suggestions = []
        if avg_att < 65:
            suggestions.append("Launch an interactive quick poll (+10% engagement boost)")
            suggestions.append("Pose a check-for-understanding question to re-center focus")
        elif avg_att >= 85:
            suggestions.append("High engagement observed; maintain current interactive pace")
            suggestions.append("Introduce a challenging hands-on code prompt for extension")
        else:
            suggestions.append("Incorporate a visual diagram or practical live code demo")
            suggestions.append("Pause for a brief 60-second peer discussion")

        if noise > -18.0:
            suggestions.append("Classroom ambient noise is high; bring attention back to podium")

        return suggestions
