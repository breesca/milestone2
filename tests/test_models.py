import pytest
from app import create_app, db
from app.models import User, Goal

@pytest.fixture
def app_instance():
    app = create_app()
    # Use an in-memory SQLite DB just for tests
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_user_goal_relationship(app_instance):
    with app_instance.app_context():
        User.query.delete()
        db.session.commit()

        user = User(email="test@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()

        goal = Goal(title="Test goal", owner=user)
        db.session.add(goal)
        db.session.commit()

        assert goal.owner == user
        assert user.goals[0].title == "Test goal"

