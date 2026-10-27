class RecommendationsEngine:
    """
    Milestone 5: Activity 5.1
    Rule-based recommendations for immediate instructor feedback.
    Input: session_status dict (people, emotions, attention, noise_level)
    Output: List of { type: 'alert' | 'warning' | 'info', message: str }
    """
    def generate_realtime_recommendations(self, session_status: dict):
        recs = []
        people = session_status.get("people", [])
        avg_att = session_status.get("avg_attention", 0.0)

        if people:
            calculated_avg = sum([p.get("attention", 75) for p in people]) / len(people)
            avg_att = avg_att or calculated_avg

            # 1. Individual Low Attention Alert
            for p in people:
                att = p.get("attention", 75)
                name = p.get("name", p.get("id", "Student"))
                if att < 40:
                    recs.append({
                        "type": "alert",
                        "message": f"Student {name} is distracted ({att:.0f}% attention)."
                    })
                elif p.get("emotion") == "tired":
                    recs.append({
                        "type": "warning",
                        "message": f"Student {name} appears fatigued or drowsy."
                    })

        # 2. Global Attention Warning
        if len(people) >= 2 and avg_att < 60:
            recs.append({
                "type": "warning",
                "message": f"Average class attention is low ({avg_att:.1f}%). Consider an interactive activity."
            })
        elif avg_att >= 85 and len(people) >= 1:
            recs.append({
                "type": "info",
                "message": f"Excellent group focus ({avg_att:.1f}%). Maintain current pace."
            })

        # 3. Audio Noise Alert
        noise_level = session_status.get("noise_level", -28.0)
        if noise_level > -15.0:
            recs.append({
                "type": "alert",
                "message": f"High acoustic noise detected ({noise_level:.1f} dB). Check for background disturbances."
            })

        return recs
