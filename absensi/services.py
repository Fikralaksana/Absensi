from flask import jsonify
from pydantic.error_wrappers import ValidationError
from flask import Blueprint
from .response import BaseResponse

bp = Blueprint('services', __name__)

@bp.app_errorhandler(ValidationError)
def resource_not_found(e:ValidationError):
    resp={}
    for i in e.errors():
        resp[i['loc'][0]]=i['msg']

    response=BaseResponse(status="error",msg=resp)
    return jsonify(response.dict()), 400

@bp.app_errorhandler(400)
def resource_not_found(e):
    response=BaseResponse(status="error",msg=str(e))
    return jsonify(response.dict()), 400
    
