from app.db.database import Base, SessionLocal, engine
from app.models import Badge, DiaryEntry, User


def test_database_connection():
    with engine.connect() as connection:
        assert connection.closed is False


def test_all_models_registered():
    assert "users" in Base.metadata.tables
    assert "diary_entries" in Base.metadata.tables
    assert "badges" in Base.metadata.tables


def test_create_and_read_user():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == "test@mindbloom.ai")
            .first()
        )

        if existing_user:
            db.delete(existing_user)
            db.commit()

        user = User(
            email="test@mindbloom.ai",
            username="testuser",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.email == "test@mindbloom.ai"
        assert user.username == "testuser"

    finally:
        db.close()


def test_create_diary_entry():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == "diary-test@mindbloom.ai")
            .first()
        )

        if existing_user:
            db.delete(existing_user)
            db.commit()

        user = User(
            email="diary-test@mindbloom.ai",
            username="diarytest",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        entry = DiaryEntry(
            user_id=user.id,
            title="My First Entry",
            content="Today was a good day.",
            mood="happy",
        )

        db.add(entry)
        db.commit()
        db.refresh(entry)

        assert entry.id is not None
        assert entry.user_id == user.id
        assert entry.title == "My First Entry"
        assert entry.mood == "happy"

    finally:
        db.close()


def test_create_badge():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == "badge-test@mindbloom.ai")
            .first()
        )

        if not user:
            user = User(
                email="badge-test@mindbloom.ai",
                username="badge_test_user",
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        existing_badge = (
            db.query(Badge)
            .filter(
                Badge.name == "First Entry",
                Badge.user_id == user.id,
            )
            .first()
        )

        if existing_badge:
            db.delete(existing_badge)
            db.commit()

        badge = Badge(
            user_id=user.id,
            name="First Entry",
            description="Created your first diary entry.",
        )

        db.add(badge)
        db.commit()
        db.refresh(badge)

        assert badge.id is not None
        assert badge.user_id == user.id
        assert badge.name == "First Entry"
        assert badge.description == "Created your first diary entry."

    finally:
        db.close()

def test_user_diary_relationship():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == "relationship@mindbloom.ai")
            .first()
        )

        if existing_user:
            db.delete(existing_user)
            db.commit()

        user = User(
            email="relationship@mindbloom.ai",
            username="relationshiptest",
        )

        entry = DiaryEntry(
            title="Relationship Test",
            content="Testing the user diary relationship.",
            mood="calm",
        )

        user.diary_entries.append(entry)

        db.add(user)
        db.commit()
        db.refresh(user)

        assert len(user.diary_entries) == 1
        assert user.diary_entries[0].title == "Relationship Test"
        assert user.diary_entries[0].user_id == user.id

    finally:
        db.close()
