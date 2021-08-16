from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from Farm.models import User, Login,Feedback, Pesticides, Crops

class RegistrationForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(),Length(min=2, max=30)])
    email = StringField('E-mail',
        validators=[DataRequired(),Email()])
    aadhaar = StringField('Aadhaar-No',
        validators=[DataRequired(),Length(min=12,max=12)])
    password = PasswordField('Password',
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('''entered email already exists,
                    try another one or login using the entered email''')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class FeedbackForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    feedback = TextAreaField('Feedback',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CropForm(FlaskForm):
    cropname = StringField('Crop_Name',validators=[DataRequired()])
    cropcost = IntegerField('Crop_Cost',validators=[DataRequired()])
    soiltype = StringField('SoilType',validators=[DataRequired()])
    submit = SubmitField('Submit')

class PesticideForm(FlaskForm):
    category = StringField('Category',validators=[DataRequired()])
    pesticidecost = IntegerField('Pesticide_Cost',validators=[DataRequired()])
    effective = StringField('Effective_On',validators=[DataRequired()])
    submit = SubmitField('Submit')

class FertilizerForm(FlaskForm):
    fertilizername = StringField('Fertilizer_Name',validators=[DataRequired()])
    fertilizercost = IntegerField('Fertilizer_Cost',validators=[DataRequired()])
    submit = SubmitField('Submit')

class BoughtForm(FlaskForm):
    submit = SubmitField('Buy')