from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import pytest

def setup_app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.create_all()
    return app

def test_index_route():
    app = setup_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome" in resp.data or b"StudyBuddy" in resp.data

def test_login_and_dashboard():
    app = setup_app()
    client = app.test_client()
    with app.app_context():
        user = User(
            email="test@example.com",
            password_hash=generate_password_hash("password123"),
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id


    with client.session_transaction() as sess:
        sess["_user_id"] = str(user_id)

    resp = client.get("/dashboard")
    assert resp.status_code == 200

