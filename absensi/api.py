from flask import Blueprint,current_app
from flask import jsonify
from flask import request
from .request import UserRegisterRequest
from .response import UserRegisterResponse
from .model import User
from sqlalchemy.orm import Session
bp = Blueprint('api', __name__, template_folder='templates')

@bp.get('/api/register')
def register():
    with Session(current_app.config['engine']) as session:
        user=UserRegisterRequest(**(request.json))
        user=User(**(user.dict()))
        session.add(user)
        session.commit()
        user.id
        response=UserRegisterResponse(**(user.__dict__)).get()
    return jsonify(response)

