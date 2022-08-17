from flask import jsonify,Blueprint,current_app,request,session
from .request import UserRegisterRequest,LoginRequest
from .response import BaseResponse,UserRegisterResponse
from .model import User
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session

bp = Blueprint('api', __name__, template_folder='templates')

@bp.get('/hello')
def hello():
    with Session(current_app.config['engine']) as session:
        response=BaseResponse().dict()
    return jsonify(response)

@bp.get('/api/register')
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

