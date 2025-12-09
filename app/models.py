from datetime import datetime

from flask_login import UserMixin
from . import db, login_manager

group_members = db.Table(
    "group_members",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("study_group.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="student")

    goals = db.relationship("Goal", backref="owner", lazy=True)

    groups = db.relationship(
        "StudyGroup",
        secondary=group_members,
        back_populates="members",
    )

    def __repr__(self):
        return f"<User {self.email}>"


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Course {self.code}>"


class StudyGroup(db.Model):
    __tablename__ = "study_group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    members = db.relationship(
        "User",
        secondary=group_members,
        back_populates="groups",
    )

    goals = db.relationship("Goal", backref="group", lazy=True)

    def __repr__(self):
        return f"<StudyGroup {self.name}>"


class Goal(db.Model):
    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    week = db.Column(db.String(20), nullable=True)  # e.g. "Week 3"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("study_group.id"), nullable=True)

    updates = db.relationship("ProgressUpdate", backref="goal", lazy=True)

    def __repr__(self):
        return f"<Goal {self.title} for user {self.user_id}>"


class ProgressUpdate(db.Model):
    __tablename__ = "progress_update"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=False)

    def __repr__(self):
        return f"<ProgressUpdate {self.id}>"


@login_manager.user_loader
def load_user(user_id: str):
    """Required by Flask-Login to load a user from the session."""
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None

