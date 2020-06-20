from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import math

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    patients = db.relationship('Patient', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    age = db.Column(db.Integer, index=True)
    name = db.Column(db.String(20), index=True)
    hospital = db.Column(db.String(140))
    mrn = db.Column(db.String(20), unique=True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    bmi = db.Column(db.Float)
    bsa = db.Column(db.Float)
    d_prednisolone = db.Column(db.Float)
    d_vincristine = db.Column(db.Float)
    d_daunorubicin = db.Column(db.Float)
    d_methotrexate = db.Column(db.Float)
    d_ecoli = db.Column(db.Float)
    d_pegaspargase = db.Column(db.Float)
    d_cotrimoxazole = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    risk_factors = db.relationship('RiskFactor', backref='author', lazy='dynamic', primaryjoin="and_(Patient.id==RiskFactor.patient_id, "
                        "Patient.age==RiskFactor.patient_age)")

    def __repr__(self):
        return '<Patient {}>'.format(self.name)

    def set_bmi(self):
        self.bmi= round((self.weight*100*100)/(self.height*self.height),2)

    def set_bsa(self):
        self.bsa= round(math.sqrt((self.height*self.weight)/3600),2)

    def set_prednisolone(self):
        Prednisolone = 60*self.bsa
        round(Prednisolone,2)
        if Prednisolone >=120:
            Prednisolone = 120
        self.d_prednisolone=Prednisolone

    def set_vincristine(self):
        Vincristine = 1.5*self.bsa
        round(Vincristine,2)
        if Vincristine >=2:
            Vincristine = 2
        self.d_vincristine=Vincristine

    def set_daunorubicin(self):
        Daunorubicin = 25*self.bsa
        round(Daunorubicin,2)
        self.d_daunorubicin=Daunorubicin

    def set_methotrexate(self):
        if self.age <= 2:
            Methotrexate = 8
        elif 2< self.age <= 3:
            Methotrexate = 10
        else:
            Methotrexate = 12
        round(Methotrexate,2)
        self.d_methotrexate=Methotrexate

    def set_ecoli(self):
        Ecoli_Asparginase = 10000*self.bsa
        round(Ecoli_Asparginase,2)
        self.d_ecoli=Ecoli_Asparginase

    def set_pegaspargase(self):
        Pegaspargase = 1000*self.bsa
        round(Pegaspargase,2)
        self.d_pegaspargase=Pegaspargase

    def set_cotrimoxazole(self):
        if 0.5 <= self.bsa <= 0.75:
            Cotrimoxazole = 240
        elif 0.76 <= self.bsa <= 1.00:
            Cotrimoxazole = 360
        else:
            Cotrimoxazole = 480
        round(Cotrimoxazole,2)
        self.d_cotrimoxazole=Cotrimoxazole

class RiskFactor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wbc = db.Column(db.Integer)
    prednisolone = db.Column(db.String(10))
    tbd = db.Column(db.String(10))
    hrcyto = db.Column(db.String(10))
    cns = db.Column(db.String(10))
    acf = db.Column(db.String(10))
    risk_type = db.Column(db.String(10), index=True)
    mrd = db.Column(db.Float)
    cr = db.Column(db.String(10))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), index=True)
    patient_age = db.Column(db.Integer, db.ForeignKey('patient.age'))

    def __repr__(self):
        return '<Risk Type {} of Patient {}>'.format(self.risk_type, self.patient_id)

    def set_default(self):
        self.prednisolone='good'
        self.mrd=0.00005
        self.cr = 'no'

    def set_risk_type(self):
        if(self.patient_age<10 and self.patient_age>1 and self.wbc<50000 and self.prednisolone=="good"
           and self.tbd=="no" and self.hrcyto=="no" and self.mrd<0.0001):
            self.risk_type = 'STANDARD'
        elif(self.patient_age>=10 and self.wbc>=50000 and self.prednisolone=="good" and
                self.tbd=="yes" and self.hrcyto=="no" and self.mrd<0.001):
            self.risk_type = 'INTERMEDIATE'
        else:
            self.risk_type = 'HIGH'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
