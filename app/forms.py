from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, max=128)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Log In")

class GoalForm(FlaskForm):
    title = StringField("Weekly Goal", validators=[DataRequired(), Length(max=255)])
    week = StringField("Week Label (e.g. Week 3)", validators=[Length(max=20)])
    submit = SubmitField("Save Goal")

class ProgressForm(FlaskForm):
    content = TextAreaField("Progress Update", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Post Update")

