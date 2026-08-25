from app.db.database import Base, SessionLocal, engine
from app.models import User


def test_database_connection():
    with engine.connect() as connection:
        assert connection.closed is False


def test_users_table_exists():
    assert "users" in Base.metadata.tables


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

        saved_user = db.get(User, user.id)

        assert saved_user is not None
        assert saved_user.email == "test@mindbloom.ai"
        assert saved_user.username == "testuser"

    finally:
        db.close()
