from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mood import MoodEntry


POSITIVE = {
    "happy", "great", "good", "excited", "calm",
    "peaceful", "grateful", "joyful", "motivated",
}

NEGATIVE = {
    "sad", "angry", "anxious", "stressed", "stress",
    "depressed", "lonely", "tired", "upset", "bad",
    "worried", "overwhelmed",
}


def analyze_wellbeing(db: Session, user_id: int) -> dict:
    result = db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.created_at.desc())
        .limit(10)
    )

    entries = list(result.scalars().all())
    moods = [entry.mood.lower().strip() for entry in entries]

    if not moods:
        return {
            "mood": "unknown",
            "total_entries": 0,
            "recent_moods": [],
            "insight": (
                "Start tracking your mood regularly so MindBloomAI "
                "can understand your wellbeing patterns."
            ),
            "wellbeing_score": 50,
            "recommendations": [
                {
                    "title": "Track your first mood",
                    "message": "Check in with yourself and record how you feel today.",
                    "category": "mood",
                    "priority": "normal",
                }
            ],
        }

    counts = Counter(moods)
    dominant_mood = counts.most_common(1)[0][0]

    positive_count = sum(mood in POSITIVE for mood in moods)
    negative_count = sum(mood in NEGATIVE for mood in moods)

    score = 60 + (positive_count * 10) - (negative_count * 10)
    score = max(0, min(100, score))

    recommendations = []

    if negative_count >= 3:
        insight = (
            "Your recent mood history shows several difficult emotional "
            "moments. Consider taking small breaks and talking to someone "
            "you trust."
        )
        recommendations.extend([
            {
                "title": "Take a mindful break",
                "message": "Spend 5 minutes breathing slowly and focusing on the present.",
                "category": "mindfulness",
                "priority": "high",
            },
            {
                "title": "Write in your diary",
                "message": "Express what is making you feel this way in your private diary.",
                "category": "journaling",
                "priority": "high",
            },
            {
                "title": "Reach out",
                "message": "If these feelings continue or become overwhelming, speak with someone you trust or a qualified professional.",
                "category": "support",
                "priority": "high",
            },
        ])
    elif positive_count >= negative_count:
        insight = (
            "Your recent mood pattern appears generally positive. "
            "Keep maintaining the habits that support your wellbeing."
        )
        recommendations.extend([
            {
                "title": "Keep your positive routine",
                "message": "Continue activities that help you feel calm and happy.",
                "category": "wellbeing",
                "priority": "normal",
            },
            {
                "title": "Practice gratitude",
                "message": "Write down one thing you are grateful for today.",
                "category": "gratitude",
                "priority": "normal",
            },
        ])
    else:
        insight = (
            "Your mood pattern has been mixed recently. Regular check-ins "
            "can help you understand what affects your wellbeing."
        )
        recommendations.extend([
            {
                "title": "Check in daily",
                "message": "Track your mood at the same time each day.",
                "category": "mood",
                "priority": "normal",
            },
            {
                "title": "Reflect on patterns",
                "message": "Use your diary to notice events connected to changes in your mood.",
                "category": "journaling",
                "priority": "normal",
            },
        ])

    return {
        "mood": dominant_mood,
        "total_entries": len(entries),
        "recent_moods": moods,
        "insight": insight,
        "wellbeing_score": score,
        "recommendations": recommendations,
    }
