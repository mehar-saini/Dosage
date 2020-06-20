from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Patient, RiskFactor

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    hospital = StringField('Hospital', validators=[DataRequired()])
    mrn = StringField('Medical Record Number', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    submit = SubmitField('Add')

class RiskFactorForm35(FlaskForm):
    wbc = IntegerField('WBC', validators=[DataRequired()])
    prednisolone = StringField('Prednisolone (good/poor)', validators=[DataRequired()])
    tbd = StringField('Testicular Bulky Disease (yes/no)', validators=[DataRequired()])
    hrcyto = StringField('HR Cytogenetics (yes/no)', validators=[DataRequired()])
    cns = StringField('CNS Disease (yes/no)', validators=[DataRequired()])
    acf = StringField('Atypical Clinic Feature (yes/no)', validators=[DataRequired()])
    mrd = DecimalField('MRD at day 35')
    cr = StringField('CR at day 35 (yes/no)')
    submit = SubmitField('Save')

class RiskFactorForm8(FlaskForm):
    wbc = IntegerField('WBC', validators=[DataRequired()])
    prednisolone = StringField('Prednisolone (good/poor)', validators=[DataRequired()])
    tbd = StringField('Testicular Bulky Disease (yes/no)', validators=[DataRequired()])
    hrcyto = StringField('HR Cytogenetics (yes/no)', validators=[DataRequired()])
    cns = StringField('CNS Disease (yes/no)', validators=[DataRequired()])
    acf = StringField('Atypical Clinic Feature (yes/no)', validators=[DataRequired()])
    submit = SubmitField('Save')

class RiskFactorForm(FlaskForm):
    wbc = IntegerField('WBC', validators=[DataRequired()])
    tbd = StringField('Testicular Bulky Disease (yes/no)', validators=[DataRequired()])
    hrcyto = StringField('HR Cytogenetics (yes/no)', validators=[DataRequired()])
    cns = StringField('CNS Disease (yes/no)', validators=[DataRequired()])
    acf = StringField('Atypical Clinic Feature (yes/no)', validators=[DataRequired()])
    submit = SubmitField('Save')
