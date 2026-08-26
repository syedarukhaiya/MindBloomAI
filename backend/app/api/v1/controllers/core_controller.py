from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import (
    User,
    MoodEntry,
    DiaryEntry,
    Conversation,
    Message,
    SafetyEvent,
    Activity,
    ActivityCompletion,
    Reminder,
    UserGamification,
    Achievement,
    UserAchievement,
    AIMemory,
    UserPreference,
    TrustedContact,
    SupportResource,
)
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.mood import MoodCreate, MoodResponse
from app.schemas.diary import (
    DiaryCreate,
    DiaryUpdate,
    DiaryResponse,
)
from app.schemas.reminder import (
    ReminderCreate,
    ReminderResponse,
)
from app.schemas.wellbeing import (
    ChatRequest,
    ChatResponse,
    ReflectionRequest,
    SafetyRequest,
    ContactCreate,
    PreferenceUpdate,
)

from app.security.dependencies import get_current_user
from app.services.auth_service import (
    register_user,
    authenticate_user,
    token_for,
)
from app.services.safety_service import (
    classify,
    RiskLevel,
    escalation_message,
)
from app.services.context_service import build_context
from app.services.ai_service import AIService
from app.services.local_ai_fallback import (
    chat_fallback,
    reflection_fallback,
)


router = APIRouter()


# ============================================================
# HELPERS
# ============================================================


def get_authenticated_user(
    user: User = Depends(get_current_user),
) -> User:
    return user


def utc_now() -> datetime:
    """
    Return a timezone-aware UTC datetime.
    """
    return datetime.now(timezone.utc)


def award(
    db: Session,
    user_id: int,
    points: int,
) -> UserGamification:
    """
    Add gamification points to a user.

    Does not commit immediately. The caller controls
    the transaction.
    """
    profile = db.scalar(
        select(UserGamification).where(
            UserGamification.user_id == user_id
        )
    )

    if profile is None:
        profile = UserGamification(
            user_id=user_id,
            points=0,
            level=1,
        )
        db.add(profile)
        db.flush()

    profile.points = (profile.points or 0) + points
    profile.level = max(
        1,
        profile.points // 100 + 1,
    )

    return profile


# ============================================================
# AUTH
# ============================================================


@router.post(
    "/auth/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        user = register_user(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    token = token_for(user)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/auth/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    token = token_for(user)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post("/auth/logout")
def logout():
    return {
        "ok": True,
        "message": "Session can be cleared by the client.",
    }


@router.get(
    "/auth/me",
    response_model=UserResponse,
)
def me(
    user: User = Depends(get_authenticated_user),
):
    return user


# ============================================================
# MOODS
# ============================================================


@router.post(
    "/moods",
    response_model=MoodResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_mood(
    data: MoodCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    mood = MoodEntry(
        user_id=user.id,
        **data.model_dump(),
    )

    db.add(mood)

    try:
        award(db, user.id, 10)
        db.commit()
        db.refresh(mood)
    except Exception:
        db.rollback()
        raise

    return mood


@router.get(
    "/moods",
    response_model=list[MoodResponse],
)
def get_moods(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    return db.scalars(
        select(MoodEntry)
        .where(MoodEntry.user_id == user.id)
        .order_by(MoodEntry.created_at.desc())
        .limit(100)
    ).all()


# ============================================================
# DIARY
# ============================================================


@router.post(
    "/diary",
    response_model=DiaryResponse,
    status_code=status.HTTP_201_CREATED,
)
def diary_create(
    data: DiaryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    diary_entry = DiaryEntry(
        user_id=user.id,
        **data.model_dump(),
    )

    db.add(diary_entry)

    try:
        award(db, user.id, 15)
        db.commit()
        db.refresh(diary_entry)
    except Exception:
        db.rollback()
        raise

    return diary_entry


@router.get(
    "/diary",
    response_model=list[DiaryResponse],
)
def diaries(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    return db.scalars(
        select(DiaryEntry)
        .where(DiaryEntry.user_id == user.id)
        .order_by(DiaryEntry.created_at.desc())
    ).all()


@router.get(
    "/diary/{entry_id}",
    response_model=DiaryResponse,
)
def diary_get(
    entry_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    diary_entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == entry_id,
            DiaryEntry.user_id == user.id,
        )
    )

    if diary_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    return diary_entry


@router.put(
    "/diary/{entry_id}",
    response_model=DiaryResponse,
)
def diary_put(
    entry_id: int,
    data: DiaryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    diary_entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == entry_id,
            DiaryEntry.user_id == user.id,
        )
    )

    if diary_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(diary_entry, field, value)

    db.commit()
    db.refresh(diary_entry)

    return diary_entry


@router.delete(
    "/diary/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def diary_delete(
    entry_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    diary_entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == entry_id,
            DiaryEntry.user_id == user.id,
        )
    )

    if diary_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    db.delete(diary_entry)
    db.commit()

    return None


# ============================================================
# BLOOM CHAT
# ============================================================


@router.post(
    "/bloom/chat",
    response_model=ChatResponse,
)
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    input_risk = classify(data.message)

    conversation_obj = None

    # --------------------------------------------------------
    # Existing conversation
    # --------------------------------------------------------

    if data.conversation_id is not None:
        conversation_obj = db.scalar(
            select(Conversation).where(
                Conversation.id == data.conversation_id,
                Conversation.user_id == user.id,
            )
        )

        if conversation_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

    # --------------------------------------------------------
    # Create conversation
    # --------------------------------------------------------

    if conversation_obj is None:
        conversation_obj = Conversation(
            user_id=user.id,
            listener_mode=data.listener_mode,
            language=data.language,
            title="Talk with Bloom",
        )

        db.add(conversation_obj)
        db.flush()

    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    user_message = Message(
        conversation_id=conversation_obj.id,
        role="user",
        content=data.message,
        risk_level=input_risk.value,
    )

    db.add(user_message)

    evidence: list[str] = []
    escalation = False
    output_risk = input_risk

    # --------------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------------

    if input_risk == RiskLevel.HIGH_RISK:
        answer = escalation_message()
        provider = "safety-policy"
        escalation = True

    # --------------------------------------------------------
    # NORMAL / DISTRESS
    # --------------------------------------------------------

    else:
        context = build_context(db, user.id)

        if context.get("recent_moods"):
            evidence.append(
                "Recent mood check-ins: "
                + ", ".join(
                    str(mood)
                    for mood in context["recent_moods"][:3]
                )
            )

        if context.get("recent_themes"):
            evidence.append(
                "Recent reflection themes include: "
                + ", ".join(
                    str(theme)
                    for theme in context["recent_themes"]
                )
            )

        try:
            answer, provider = AIService().chat(
                data.message,
                context,
                data.listener_mode,
                data.language,
            )

        except Exception:
            answer = chat_fallback(
                data.message,
                data.listener_mode,
                data.language,
            )
            provider = "development-fallback"

        # ----------------------------------------------------
        # AI output safety check
        # ----------------------------------------------------

        output_risk = classify(answer)

        if output_risk == RiskLevel.HIGH_RISK:
            answer = escalation_message()
            provider = "safety-postcheck"
            escalation = True

    # --------------------------------------------------------
    # Assistant message
    # --------------------------------------------------------

    assistant_message = Message(
        conversation_id=conversation_obj.id,
        role="assistant",
        content=answer,
        risk_level=output_risk.value,
    )

    db.add(assistant_message)

    # --------------------------------------------------------
    # Safety event
    # --------------------------------------------------------

    if input_risk != RiskLevel.NORMAL:
        db.add(
            SafetyEvent(
                user_id=user.id,
                risk_level=input_risk.value,
                source="precheck",
            )
        )

    if output_risk == RiskLevel.HIGH_RISK and input_risk != RiskLevel.HIGH_RISK:
        db.add(
            SafetyEvent(
                user_id=user.id,
                risk_level=output_risk.value,
                source="postcheck",
            )
        )

    db.commit()

    return ChatResponse(
        conversation_id=conversation_obj.id,
        message=answer,
        risk_level=input_risk.value,
        safety_escalation=escalation,
        context_used=(
            ["recent moods", "recent reflections"]
            if evidence
            else []
        ),
        evidence=evidence,
        suggested_action=(
            {
                "title": "60-second reset",
                "slug": "one_minute_reset",
            }
            if input_risk == RiskLevel.DISTRESS
            else None
        ),
        provider=provider,
    )


@router.get("/bloom/conversations")
def conversations(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    items = db.scalars(
        select(Conversation)
        .where(Conversation.user_id == user.id)
        .order_by(Conversation.created_at.desc())
    ).all()

    return [
        {
            "id": item.id,
            "title": item.title,
            "listener_mode": item.listener_mode,
            "language": item.language,
            "created_at": item.created_at,
        }
        for item in items
    ]


@router.get("/bloom/conversations/{conversation_id}")
def conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    conversation_obj = db.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )

    if conversation_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages = db.scalars(
        select(Message)
        .where(
            Message.conversation_id == conversation_obj.id
        )
        .order_by(Message.created_at)
    ).all()

    return {
        "id": conversation_obj.id,
        "title": conversation_obj.title,
        "listener_mode": conversation_obj.listener_mode,
        "language": conversation_obj.language,
        "created_at": conversation_obj.created_at,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "risk_level": message.risk_level,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }


@router.post("/bloom/reflection")
def reflection(
    data: ReflectionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    diary_entry = db.scalar(
        select(DiaryEntry).where(
            DiaryEntry.id == data.diary_entry_id,
            DiaryEntry.user_id == user.id,
        )
    )

    if diary_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diary entry not found",
        )

    # Use the user's saved language where available.
    preference = db.scalar(
        select(UserPreference).where(
            UserPreference.user_id == user.id
        )
    )

    language = (
        preference.language
        if preference and preference.language
        else "English"
    )

    try:
        text = AIService().reflection(
            diary_entry.content,
            language,
        )
        provider = "google-cloud-gemini"

    except Exception:
        text = reflection_fallback()
        provider = "development-fallback"

    return {
        "reflection": text,
        "provider": provider,
        "source_diary_id": diary_entry.id,
    }


# ============================================================
# SAFETY
# ============================================================


@router.post("/safety/analyze")
def safety(
    data: SafetyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    risk = classify(data.message)

    db.add(
        SafetyEvent(
            user_id=user.id,
            risk_level=risk.value,
            source="manual",
        )
    )

    db.commit()

    return {
        "risk_level": risk.value,
        "escalation": risk == RiskLevel.HIGH_RISK,
        "message": (
            escalation_message()
            if risk == RiskLevel.HIGH_RISK
            else "No high-risk signal detected by the lightweight pre-check."
        ),
    }


# ============================================================
# WELLBEING
# ============================================================


@router.get("/wellbeing/insights")
def insights(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    mood_entries = db.scalars(
        select(MoodEntry)
        .where(MoodEntry.user_id == user.id)
        .order_by(MoodEntry.created_at.desc())
        .limit(10)
    ).all()

    moods = [entry.mood for entry in mood_entries]

    negative_moods = {
        "Very low",
        "Low",
        "Sad",
        "Anxious",
        "Stressed",
        "Overwhelmed",
    }

    positive_moods = {
        "Good",
        "Great",
        "Happy",
        "Calm",
    }

    positive_count = sum(
        mood in positive_moods
        for mood in moods
    )

    negative_count = sum(
        mood in negative_moods
        for mood in moods
    )

    wellbeing_score = max(
        0,
        min(
            100,
            50 + positive_count * 8 - negative_count * 8,
        ),
    )

    if moods:
        insight = (
            "A pattern worth noticing is that your recent "
            "check-ins are mixed; regular reflection can help "
            "you notice what supports you."
        )
    else:
        insight = "Start with one gentle check-in today."

    return {
        "mood": moods[0] if moods else "unknown",
        "total_entries": len(moods),
        "recent_moods": moods,
        "insight": insight,
        "wellbeing_score": wellbeing_score,
        "recommendations": [
            {
                "title": "60-second reset",
                "message": (
                    "Slow your breathing and make the next "
                    "minute smaller."
                ),
                "category": "mindfulness",
                "priority": "normal",
            },
            {
                "title": "Write it down",
                "message": (
                    "Use your private diary to put one "
                    "thought into words."
                ),
                "category": "reflection",
                "priority": "normal",
            },
        ],
    }


@router.get("/wellbeing/trends")
def trends(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    mood_entries = db.scalars(
        select(MoodEntry)
        .where(MoodEntry.user_id == user.id)
        .order_by(MoodEntry.created_at)
    ).all()

    return [
        {
            "date": (
                entry.created_at.date().isoformat()
                if entry.created_at
                else None
            ),
            "mood": entry.mood,
            "stress": entry.stress,
            "energy": entry.energy,
        }
        for entry in mood_entries
    ]


@router.get("/wellbeing/weekly-summary")
def weekly(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    since = utc_now() - timedelta(days=7)

    mood_entries = db.scalars(
        select(MoodEntry).where(
            MoodEntry.user_id == user.id,
            MoodEntry.created_at >= since,
        )
    ).all()

    diary_entries = db.scalars(
        select(DiaryEntry).where(
            DiaryEntry.user_id == user.id,
            DiaryEntry.created_at >= since,
        )
    ).all()

    completed_activities = db.scalars(
        select(ActivityCompletion).where(
            ActivityCompletion.user_id == user.id,
            ActivityCompletion.completed_at >= since,
        )
    ).all()

    difficult_moods = {
        "Low",
        "Very low",
        "Anxious",
        "Stressed",
    }

    return {
        "checkins": len(mood_entries),
        "reflections": len(diary_entries),
        "activities_completed": len(completed_activities),
        "what_went_well": (
            "You made space for reflection."
            if diary_entries
            else "Try one small reflection this week."
        ),
        "difficult_moments": (
            "Your check-ins show that some days felt harder."
            if any(
                entry.mood in difficult_moods
                for entry in mood_entries
            )
            else "No difficult mood label was recorded this week."
        ),
        "next_step": (
            "Choose one small, repeatable action "
            "for the coming week."
        ),
        "prompt": "What helped even a little this week?",
    }


@router.get("/wellbeing/weekly-reflection")
def weekly_reflection(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    since = utc_now() - timedelta(days=7)

    mood_entries = db.scalars(
        select(MoodEntry).where(
            MoodEntry.user_id == user.id,
            MoodEntry.created_at >= since,
        )
    ).all()

    diary_entries = db.scalars(
        select(DiaryEntry).where(
            DiaryEntry.user_id == user.id,
            DiaryEntry.created_at >= since,
        )
    ).all()

    mood_names = [
        entry.mood
        for entry in mood_entries
    ]

    diary_titles = [
        entry.title
        for entry in diary_entries
    ]

    summary = (
        f"Check-ins: {len(mood_entries)}. "
        f"Moods: {mood_names}. "
        f"Reflections: {diary_titles}."
    )

    prompt = (
        "You are Bloom. Write a concise, non-diagnostic "
        "weekly wellbeing reflection. Use only the supplied "
        "data. Mention what went well, what felt difficult, "
        "one next step, and one reflection prompt."
    )

    try:
        text = AIService().provider.generate(
            prompt,
            summary,
        )
        provider = "google-cloud-gemini"

    except Exception:
        text = (
            "What went well: You made space to check in.\n\n"
            "What felt difficult: Some moments may have felt "
            "heavier than others.\n\n"
            "Next step: Choose one small repeatable action.\n\n"
            "Prompt: What helped even a little this week?"
        )
        provider = "development-fallback"

    return {
        "reflection": text,
        "provider": provider,
        "source_counts": {
            "checkins": len(mood_entries),
            "reflections": len(diary_entries),
        },
    }


# ============================================================
# ACTIVITIES & RECOMMENDATIONS
# ============================================================


@router.get("/recommendations")
def recommendations(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    activities = db.scalars(
        select(Activity)
    ).all()

    return activities


@router.post("/activities/{activity_id}/complete")
def activity_complete(
    activity_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    activity = db.get(Activity, activity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    # Prevent accidental duplicate completion.
    existing = db.scalar(
        select(ActivityCompletion).where(
            ActivityCompletion.user_id == user.id,
            ActivityCompletion.activity_id == activity.id,
        )
    )

    if existing is not None:
        return {
            "ok": True,
            "already_completed": True,
            "activity": activity.title,
            "message": "This activity has already been completed.",
        }

    completion = ActivityCompletion(
        user_id=user.id,
        activity_id=activity.id,
    )

    db.add(completion)
    award(db, user.id, 10)

    db.commit()

    return {
        "ok": True,
        "already_completed": False,
        "activity": activity.title,
        "message": "Small step complete. Consistency, not perfection.",
    }


# ============================================================
# REMINDERS
# ============================================================


@router.get(
    "/reminders",
    response_model=list[ReminderResponse],
)
def reminders(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    return db.scalars(
        select(Reminder)
        .where(Reminder.user_id == user.id)
        .order_by(Reminder.reminder_time)
    ).all()


@router.post(
    "/reminders",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
def reminder(
    data: ReminderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    reminder_obj = Reminder(
        user_id=user.id,
        **data.model_dump(),
    )

    db.add(reminder_obj)
    db.commit()
    db.refresh(reminder_obj)

    return reminder_obj


@router.delete(
    "/reminders/{rid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reminder_delete(
    rid: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    reminder_obj = db.scalar(
        select(Reminder).where(
            Reminder.id == rid,
            Reminder.user_id == user.id,
        )
    )

    if reminder_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found",
        )

    db.delete(reminder_obj)
    db.commit()

    return None


# ============================================================
# GAMIFICATION
# ============================================================


@router.get("/gamification")
def gamification(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    profile = db.scalar(
        select(UserGamification).where(
            UserGamification.user_id == user.id
        )
    )

    if profile is None:
        profile = UserGamification(
            user_id=user.id,
            points=0,
            level=1,
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

    achievements = db.scalars(
        select(Achievement)
        .join(
            UserAchievement,
            UserAchievement.achievement_id == Achievement.id,
        )
        .where(
            UserAchievement.user_id == user.id
        )
    ).all()

    return {
        "profile": {
            "user_id": user.id,
            "points": profile.points,
            "level": profile.level,
            "current_streak": profile.current_streak,
            "longest_streak": profile.longest_streak,
            "last_activity_date": profile.last_activity_date,
        },
        "achievements": [
            {
                "id": achievement.id,
                "code": achievement.code,
                "name": achievement.name,
                "description": achievement.description,
                "points_required": achievement.points_required,
            }
            for achievement in achievements
        ],
    }


@router.get("/gamification/garden")
def garden(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    profile = db.scalar(
        select(UserGamification).where(
            UserGamification.user_id == user.id
        )
    )

    points = profile.points if profile else 0
    level = profile.level if profile else 1

    return {
        "level": level,
        "points": points,
        "growth": min(100, points % 100),
        "message": (
            "Your garden isn't going anywhere. "
            "You can start again today."
        ),
    }


# ============================================================
# PRIVACY / MEMORY
# ============================================================


@router.get("/privacy/memory")
def memory(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    memories = db.scalars(
        select(AIMemory)
        .where(AIMemory.user_id == user.id)
        .order_by(AIMemory.created_at.desc())
    ).all()

    return {
        "memory_enabled": True,
        "items": [
            {
                "id": item.id,
                "memory": item.memory,
                "source": item.source,
                "created_at": item.created_at,
            }
            for item in memories
        ],
    }


@router.delete(
    "/privacy/memory/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def memory_delete(
    memory_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    memory_item = db.scalar(
        select(AIMemory).where(
            AIMemory.id == memory_id,
            AIMemory.user_id == user.id,
        )
    )

    if memory_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    db.delete(memory_item)
    db.commit()

    return None


@router.get("/privacy/export")
def export_data(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    moods = db.scalars(
        select(MoodEntry).where(
            MoodEntry.user_id == user.id
        )
    ).all()

    diary_entries = db.scalars(
        select(DiaryEntry).where(
            DiaryEntry.user_id == user.id
        )
    ).all()

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        },
        "moods": [
            {
                "mood": mood.mood,
                "note": mood.note,
                "created_at": mood.created_at,
            }
            for mood in moods
        ],
        "diary": [
            {
                "title": entry.title,
                "content": entry.content,
                "created_at": entry.created_at,
            }
            for entry in diary_entries
        ],
    }


@router.delete(
    "/privacy/account",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_account(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    # --------------------------------------------------------
    # Find conversations
    # --------------------------------------------------------

    conversation_ids = db.scalars(
        select(Conversation.id).where(
            Conversation.user_id == user.id
        )
    ).all()

    # --------------------------------------------------------
    # Delete messages first
    # --------------------------------------------------------

    if conversation_ids:
        db.query(Message).filter(
            Message.conversation_id.in_(conversation_ids)
        ).delete(
            synchronize_session=False
        )

    # --------------------------------------------------------
    # Delete conversations
    # --------------------------------------------------------

    db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).delete(
        synchronize_session=False
    )

    # --------------------------------------------------------
    # Delete user-owned data
    # --------------------------------------------------------

    user_owned_models = [
        AIMemory,
        UserPreference,
        TrustedContact,
        SafetyEvent,
        ActivityCompletion,
        DiaryEntry,
        MoodEntry,
        Reminder,
        UserGamification,
    ]

    for model in user_owned_models:
        db.query(model).filter(
            getattr(model, "user_id") == user.id
        ).delete(
            synchronize_session=False
        )

    # --------------------------------------------------------
    # Delete achievements
    # --------------------------------------------------------

    db.query(UserAchievement).filter(
        UserAchievement.user_id == user.id
    ).delete(
        synchronize_session=False
    )

    # --------------------------------------------------------
    # Finally delete user
    # --------------------------------------------------------

    db.delete(user)
    db.commit()

    return None


# ============================================================
# SUPPORT
# ============================================================


@router.get("/support/resources")
def support_resources(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    return db.scalars(
        select(SupportResource).where(
            SupportResource.verified.is_(True)
        )
    ).all()


@router.get("/support/providers")
def support_providers(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    return {
        "items": [],
        "message": (
            "Provider listings require a verified directory "
            "integration; no provider is fabricated by MindBloomAI."
        ),
    }


@router.get("/support/contacts")
def contacts(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    return db.scalars(
        select(TrustedContact).where(
            TrustedContact.user_id == user.id
        )
    ).all()


@router.post("/support/contacts")
def contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    trusted_contact = TrustedContact(
        user_id=user.id,
        **data.model_dump(),
    )

    db.add(trusted_contact)
    db.commit()
    db.refresh(trusted_contact)

    return trusted_contact


@router.delete(
    "/support/contacts/{cid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def contact_delete(
    cid: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    trusted_contact = db.scalar(
        select(TrustedContact).where(
            TrustedContact.id == cid,
            TrustedContact.user_id == user.id,
        )
    )

    if trusted_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trusted contact not found",
        )

    db.delete(trusted_contact)
    db.commit()

    return None


# ============================================================
# DEMO SESSION
# ============================================================


@router.post("/demo/session")
def demo_session(
    db: Session = Depends(get_db),
):
    email = "demo@mindbloom.local"
    username = "Demo Bloom"

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        from app.services.auth_service import hasher

        user = User(
            email=email,
            username=username,
            password_hash=hasher.hash(
                "DemoMindBloom2026!"
            ),
        )

        db.add(user)
        db.flush()

        demo_moods = [
            ("Okay", 3, 3),
            ("Low", 4, 2),
            ("Anxious", 4, 2),
            ("Good", 2, 4),
            ("Great", 1, 5),
        ]

        for mood_name, stress, energy in demo_moods:
            db.add(
                MoodEntry(
                    user_id=user.id,
                    mood=mood_name,
                    stress=stress,
                    energy=energy,
                    context="demo",
                )
            )

        db.add(
            DiaryEntry(
                user_id=user.id,
                title="Placement pressure",
                content=(
                    "I have been thinking about exams and "
                    "placement expectations. I want to do well "
                    "without feeling like my whole future depends "
                    "on one result."
                ),
                mood="Anxious",
            )
        )

        db.commit()
        db.refresh(user)

    return {
        "access_token": token_for(user),
        "demo": True,
        "notice": (
            "DEMO DATA — this account is separate from "
            "real user data."
        ),
    }


# ============================================================
# PREFERENCES
# ============================================================


@router.get("/preferences")
def preferences(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    preference = db.scalar(
        select(UserPreference).where(
            UserPreference.user_id == user.id
        )
    )

    if preference is None:
        preference = UserPreference(
            user_id=user.id
        )

        db.add(preference)
        db.commit()
        db.refresh(preference)

    return {
        "language": preference.language,
        "tone": preference.tone,
        "memory_enabled": preference.memory_enabled,
        "reminders_enabled": preference.reminders_enabled,
        "quiet_hours": preference.quiet_hours,
    }


@router.put("/preferences")
def preferences_put(
    data: PreferenceUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    preference = db.scalar(
        select(UserPreference).where(
            UserPreference.user_id == user.id
        )
    )

    if preference is None:
        preference = UserPreference(
            user_id=user.id
        )
        db.add(preference)

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(preference, field, value)

    db.commit()
    db.refresh(preference)

    return {
        "language": preference.language,
        "tone": preference.tone,
        "memory_enabled": preference.memory_enabled,
        "reminders_enabled": preference.reminders_enabled,
        "quiet_hours": preference.quiet_hours,
    }