from flask import jsonify,session,g
from pydantic.error_wrappers import ValidationError
from flask import Blueprint,current_app
from .response import BaseResponse
from .errors import LoginFailed,AuthFailed,EmptyQuery
from sqlalchemy.orm import Session
from .model import User
import hashlib,functools

bp = Blueprint('services', __name__)

@bp.app_errorhandler(ValidationError)
def validation_error(e:ValidationError):
    resp={}
    for i in e.errors():
        resp[i['loc'][0]]=i['msg']

    response=BaseResponse(status="error",msg=resp)
    return jsonify(response.dict()), 400

@bp.app_errorhandler(LoginFailed)
def login_error(e:LoginFailed):
    response=BaseResponse(status="error",msg=str(e))
    return jsonify(response.dict()), 400

@bp.app_errorhandler(AuthFailed)
def auth_error(e:AuthFailed):
    response=BaseResponse(status="error",msg=str(e))
    return jsonify(response.dict()), 400

@bp.app_errorhandler(EmptyQuery)
def aquery_error(e:EmptyQuery):
    response=BaseResponse(status="error",msg=str(e))
    return jsonify(response.dict()), 400

@bp.app_errorhandler(400)
def resource_not_found(e):
    response=BaseResponse(status="error",msg=str(e))
    return jsonify(response.dict()), 400
    
def hash_password(inp):
    salt = "5gz"
    password= inp+salt
    h = hashlib.md5(password.encode())
    return(h.hexdigest())
    
@bp.before_app_request
def load_logged_in_user():
    with Session(current_app.config['engine']) as db_session:
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = User.get(db_session,user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            raise AuthFailed("Session Kadaluarsa")
        return view(**kwargs)

    return wrapped_view

