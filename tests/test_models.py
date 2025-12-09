import pytest
from app import create_app, db
from app.models import User, Goal

@pytest.fixture
def app_instance():
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

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

