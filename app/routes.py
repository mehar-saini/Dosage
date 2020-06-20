from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PatientForm, RiskFactorForm
from flask_login import current_user, login_user
from app.models import User, Patient, RiskFactor
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
import itertools

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = url_for('user', username=current_user.username)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    patients = user.patients.all()
    current_time = datetime.now()
    return render_template('user.html', username=username, patients=patients, current_time=current_time, len=len(patients))

@app.route('/add/<username>', methods=['GET', 'POST'])
@login_required
def add(username):
    form = PatientForm()
    if form.validate_on_submit():
        patient= Patient(name=form.name.data, age=form.age.data, hospital=form.hospital.data, mrn=form.mrn.data, height=form.height.data, weight=form.weight.data, user_id=User.query.filter_by(username=username).first().id)
        patient.set_bmi()
        patient.set_bsa()
        patient.set_ecoli()
        patient.set_vincristine()
        patient.set_daunorubicin()
        patient.set_methotrexate()
        patient.set_pegaspargase()
        patient.set_prednisolone()
        patient.set_cotrimoxazole()
        db.session.add(patient)
        db.session.commit()
        flash('Patient added!')
        return redirect(url_for('edit', username=username, name=patient.name))
    return render_template('patient.html', title='Patient', form=form)

@app.route('/edit/<username>/<name>', methods=['GET', 'POST'])
@login_required
def edit(username, name):
    user = User.query.filter_by(username=username).first_or_404()
    patient = Patient.query.filter_by(name=name, user_id=user.id).first()
    current_day = (datetime.now()-patient.timestamp).days
    form = RiskFactorForm()
    if current_day==8:
        form=RiskFactorForm8()
    elif current_day==35:
        form=RiskFactorForm35()
    if form.validate_on_submit():
        risk_factor= RiskFactor(wbc=form.wbc.data, tbd=form.tbd.data, hrcyto=form.hrcyto.data, cns=form.cns.data, acf=form.acf.data, patient_id=Patient.query.filter_by(name=name).first().id, patient_age=Patient.query.filter_by(name=name).first().age)
        risk_factor.set_default()
        if current_day==8:
            risk_factor= RiskFactor(wbc=form.wbc.data, prednisolone=form.prednisolone.data, tbd=form.tbd.data, hrcyto=form.hrcyto.data, cns=form.cns.data, acf=form.acf.data, patient_id=Patient.query.filter_by(name=name).first().id, patient_age=Patient.query.filter_by(name=name).first().age)
        if current_day==35:
            risk_factor= RiskFactor(wbc=form.wbc.data, prednisolone=form.prednisolone.data, tbd=form.tbd.data, hrcyto=form.hrcyto.data, cns=form.cns.data, acf=form.acf.data, mrd=form.mrd.data, cr=form.cr.data, patient_id=Patient.query.filter_by(name=name).first().id, patient_age=Patient.query.filter_by(name=name).first().age)
        risk_factor.set_risk_type()
        db.session.add(risk_factor)
        db.session.commit()
        flash('Risk factors edited!')
        return redirect(url_for('user', username=username))
    return render_template('risk_factor.html', title='RiskFactor', form=form)

@app.route('/info/<username>/<name>', methods=['GET', 'POST'])
@login_required
def info(username, name):
    user = User.query.filter_by(username=username).first_or_404()
    patient = Patient.query.filter_by(name=name, user_id=user.id).first()
    exists = RiskFactor.query.filter_by(patient_id=patient.id).first() is not None
    current_time = datetime.now()
    if not exists:
        flash('Add risk factors first!')
        return redirect(url_for('user', username=username))
    risk_factor = RiskFactor.query.filter_by(patient_id=patient.id).first()
    return render_template('info.html', username=username, patient=patient, risk_factor=risk_factor, current_time=current_time)
