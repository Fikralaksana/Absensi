
import sqlalchemy as db
from sqlalchemy import select,and_
from sqlalchemy.orm import declarative_base,Session
from .errors import LoginFailed
from werkzeug.security import check_password_hash

Base=declarative_base()


class BaseModel(object):
    @classmethod
    def create(cls,session,**kwargs):
        obj=cls(**kwargs)
        return obj


class User(Base,BaseModel):
    pass
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def validate_user(cls,session:Session,request):
        result=session.execute(select(cls).filter(cls.username==request.username)).first()
        if not result:
            raise LoginFailed("User tidak ditemukan")
        right=check_password_hash(result[0].password,request.password)
        if not right:
            raise LoginFailed("Password Salah")
        return result[0]
