from flask_wtf import Form
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, StringField, FileField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class UploadForm(Form):
    file = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'Somente PDF!')
    ])
    submit = SubmitField("Enviar")


class LoginForm(Form):
    name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
