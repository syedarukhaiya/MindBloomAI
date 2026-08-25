from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.gamification import (
    Achievement,
    UserAchievement,
    UserGamification,
)


def get_or_create_profile(
    db: Session,
    user_id: int,
) -> UserGamification:
    profile = db.scalar(
        select(UserGamification).where(
            UserGamification.user_id == user_id
        )
    )

    if profile is None:
        profile = UserGamification(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


def calculate_level(points: int) -> int:
    return max(1, points // 100 + 1)


def update_streak(profile: UserGamification) -> None:
    today = date.today()
    today_value = today.isoformat()

    if profile.last_activity_date == today_value:
        return

    if profile.last_activity_date:
        last_date = date.fromisoformat(profile.last_activity_date)

        if (today - last_date).days == 1:
            profile.current_streak += 1
        else:
            profile.current_streak = 1
    else:
        profile.current_streak = 1

    profile.longest_streak = max(
        profile.longest_streak,
        profile.current_streak,
    )
    profile.last_activity_date = today_value


def add_points(
    db: Session,
    user_id: int,
    points: int,
) -> UserGamification:
    profile = get_or_create_profile(db, user_id)

    profile.points = max(0, profile.points + points)
    profile.level = calculate_level(profile.points)

    update_streak(profile)

    db.commit()
    db.refresh(profile)

    unlock_achievements(db, user_id, profile.points)

    return profile


def unlock_achievements(
    db: Session,
    user_id: int,
    points: int,
) -> None:
    achievements = db.scalars(
        select(Achievement).where(
            Achievement.points_required <= points
        )
    ).all()

    unlocked_ids = set(
        db.scalars(
            select(UserAchievement.achievement_id).where(
                UserAchievement.user_id == user_id
            )
        ).all()
    )

    for achievement in achievements:
        if achievement.id not in unlocked_ids:
            db.add(
                UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id,
                )
            )

    db.commit()


def get_dashboard(
    db: Session,
    user_id: int,
):
    profile = get_or_create_profile(db, user_id)

    achievements = db.scalars(
        select(Achievement)
        .join(
            UserAchievement,
            UserAchievement.achievement_id == Achievement.id,
        )
        .where(UserAchievement.user_id == user_id)
    ).all()

    return profile, achievements
