from flask import jsonify,Blueprint,current_app,request,session
from .request import UserRegisterRequest,LoginRequest,CreateActivityRequest,UpdateActivityRequest
from .response import (Base, CreateActivityResponse,UserRegisterResponse,CheckinResponse,HistoryResponse,History,ActivitySchema,
ActivityResponse,CreateActivityResponse,UpdateActivityResponse,DeleteActivityResponse)
from .model import User,Absensi,Activity
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
import datetime
from .services import login_required,between_checkin_checkout
from .errors import EmptyQuery
from pydantic import parse_obj_as

bp = Blueprint('api', __name__, template_folder='templates')


@bp.get('/hello')
def hello():
    with Session(current_app.config['engine']) as session:
        response=Base().dict()
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
        response=Base(msg="Login Success")
    return jsonify(response.dict())

@bp.get('/api/logout')
def logout():
    with Session(current_app.config['engine']) as db_session:
        session.clear()
        response=Base(msg="Logout Success")
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
            raise EmptyQuery("Anda sudah checkin hari ini")
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
            if absen.check_out:
                raise EmptyQuery("Anda sudah check out hari ini")
            absen.check_out=datetime.datetime.now()
        db_session.commit()
        absen.id
        absen.username=absen.user.username
        response=CheckinResponse(**(absen.__dict__)).get()
    return jsonify(response)

@bp.get('/api/history')
@login_required
def history():
    with Session(current_app.config['engine']) as db_session:
        absens=Absensi.get_all_by_user_id(db_session,session['user_id'])     
        absens=[History(**(absen.__dict__)) for absen in absens]        
        response=HistoryResponse(user_id=session['user_id'],history=absens).get()
    return jsonify(response)

@bp.get('/api/activitys')
@login_required
def activitys():
    with Session(current_app.config['engine']) as db_session:
        activitys=Activity.get_all_by_user_id(db_session,session['user_id'])     
        activitys=[ActivitySchema(**(activity.__dict__)) for activity in activitys]        
        response=ActivityResponse(user_id=session['user_id'],activity=activitys).get(msg="Activity List")
    return jsonify(response)

@bp.post('/api/activity')
@login_required
@between_checkin_checkout
def create_activity():
    with Session(current_app.config['engine']) as db_session:
        activity=CreateActivityRequest(**(request.json))
        activity=Activity(name=activity.name,description=activity.description,user_id=session['user_id']) 
        db_session.add(activity)     
        db_session.commit()   
        activity.id  
        response=CreateActivityResponse(**(activity.__dict__)).get(msg="Activity Created")
    return jsonify(response)

@bp.put('/api/activity/<int:id>')
@login_required
@between_checkin_checkout
def update_activity(id):
    with Session(current_app.config['engine']) as db_session:
        activity=UpdateActivityRequest(**(request.json))
        activity=Activity.update(db_session,id,name=activity.name,description=activity.description)   
        db_session.commit()   
        activity.id  
        response=UpdateActivityResponse(**(activity.__dict__)).get(msg="Activity Updated")
    return jsonify(response)

@bp.delete('/api/activity/<int:id>')
@login_required
@between_checkin_checkout
def delete_activity(id):
    with Session(current_app.config['engine']) as db_session:
        activity=Activity.delete(db_session,id)   
        db_session.commit()   
        activity.id  
        response=DeleteActivityResponse(**(activity.__dict__)).get(msg="Activity Deleted")
    return jsonify(response)


