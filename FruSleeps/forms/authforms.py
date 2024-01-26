#from flask_wtf import FlaskForm, CSRFProtect
from wtforms import Form, StringField, SubmitField, PasswordField, BooleanField
from flask_wtf.recaptcha import RecaptchaField
from wtforms import validators

class RegistrationForm(Form):
    username = StringField("Munchkin's Name", [validators.Length(min=4, max=25)],
                            render_kw={"placeholder": "Munchkin's Name"})
    email = StringField('Email Address', [validators.Length(min=6, max=35)],
                         render_kw={"placeholder": "Email"})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=20),
        
    ], render_kw={"placeholder": "New Password"})
    confirm = PasswordField('Repeat Password',
                            [validators.EqualTo('password',
                                                 message='Passwords must match')],
                             render_kw={"placeholder": "Confirm Password"})
    recaptcha = RecaptchaField()
    #accept_tos = BooleanField('Accept Terms', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField("Munchkin",
                            [validators.Length(min=4, max=25),validators.DataRequired()],
                    render_kw={"placeholder": "Munchkin"})
    password = PasswordField('Password', [
                validators.DataRequired(),
                validators.Length(min=6, max=20)],
                render_kw={"placeholder": "Password"})