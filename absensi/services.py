from flask import jsonify
from pydantic.error_wrappers import ValidationError
from flask import Blueprint
from .response import BaseResponse
from .errors import LoginFailed
import hashlib

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

@bp.app_errorhandler(400)
def resource_not_found(e):
    response=BaseResponse(status="error",msg=str(e))
    return jsonify(response.dict()), 400
    
def hash_password(inp):
    salt = "5gz"
    password= inp+salt
    h = hashlib.md5(password.encode())
    return(h.hexdigest())
    

