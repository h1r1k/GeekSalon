from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('ユーザ名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegistrationForm(FlaskForm):
    username = StringField('ユーザ名', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('新規登録')

class PostForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('投稿')