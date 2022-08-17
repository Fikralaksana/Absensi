from flask import jsonify,Blueprint,current_app,request,session
from .request import UserRegisterRequest,LoginRequest,CheckinRequest
from .response import BaseResponse,UserRegisterResponse,CheckinResponse
from .model import User,Absensi
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
import datetime
from .services import login_required
from .errors import EmptyQuery

bp = Blueprint('api', __name__, template_folder='templates')


@bp.get('/hello')
def hello():
    with Session(current_app.config['engine']) as session:
        response=BaseResponse().dict()
    return jsonify(response)

@bp.post('/api/register')
def register():
    with Session(current_app.config['engine']) as db_session:
        user=UserRegisterRequest(**(request.json))
        user.password=generate_password_hash(user.password)
        user=User(**(user.dict()))
        db_session.add(user)
        db_session.commit()
        user.id
        response=UserRegisterResponse(**(user.__dict__)).get()
    return jsonify(response)

@bp.post('/api/login')
def login():
    with Session(current_app.config['engine']) as db_session:
        user=LoginRequest(**(request.json))
        user=User.validate_user(db_session,user)
        session.clear()
        session['user_id'] = user.id
        response=BaseResponse(msg="Login Success")
    return jsonify(response.dict())

@bp.get('/api/logout')
def logout():
    with Session(current_app.config['engine']) as db_session:
        session.clear()
        response=BaseResponse(msg="Logout Success")
    return jsonify(response.dict())

@bp.get('/api/checkin')
@login_required
def checkin():
    with Session(current_app.config['engine']) as db_session:
        absen=Absensi.get_by_check_in(db_session,session['user_id'],datetime.datetime.now().date())
        if not absen:
            absen=Absensi(check_in=datetime.datetime.now(),user_id=session['user_id'])
            db_session.add(absen)
        else: 
            raise EmptyQuery("Anda sudah Checkin")
        db_session.commit()
        absen.id
        absen.username=absen.user.username
        response=CheckinResponse(**(absen.__dict__)).get()
    return jsonify(response)
@bp.get('/api/checkout')

@login_required
def checkout():
    with Session(current_app.config['engine']) as db_session:
        absen=Absensi.get_by_check_in(db_session,session['user_id'],datetime.datetime.now().date())
        
        if not absen:
            raise EmptyQuery("Anda belum check in hari ini")
        else: 
            absen.check_out=datetime.datetime.now()
        db_session.commit()
        absen.id
        absen.username=absen.user.username
        response=CheckinResponse(**(absen.__dict__)).get()
    return jsonify(response)

