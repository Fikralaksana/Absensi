
from datetime import datetime
import sqlalchemy as db
from sqlalchemy import select,update,delete,and_
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy.orm import Session as DB_Session
from .errors import LoginFailed
from flask.sessions import SessionMixin
from werkzeug.security import check_password_hash
from typing import TypeVar,Union
BaseModelType = TypeVar('BaseModelType', bound='BaseModel')

Base=declarative_base()

class BaseModel(object):
    @classmethod
    def get(cls,db_session:DB_Session,id:str,*args, **kwargs)->BaseModelType:
        result=db_session.execute(select(cls).filter(cls.id==id)).first()
        return result[0] if result else None
    @classmethod
    def get_all(cls,db_session:DB_Session,id:str,*args, **kwargs)->BaseModelType:
        results=db_session.execute(select(cls).filter(cls.id==id)).all()
        return [result[0] for result in results] if results else []
    @classmethod
    def get_by_user_id(cls,db_session:DB_Session,id:str,*args, **kwargs)->BaseModelType:
        result=db_session.execute(select(cls).filter(cls.user_id==id).filter()).first()
        return result[0] if result else None
    @classmethod
    def get_all_by_user_id(cls,db_session:DB_Session,id:str,*args, **kwargs)->BaseModelType:
        results=db_session.execute(select(cls).filter(cls.user_id==id)).all()
        return [result[0] for result in results] if results else []
    @classmethod
    def update(cls,db_session:DB_Session,id:str,*args, **kwargs)->BaseModelType:
        db_session.execute(update(cls).where(cls.id == id).values(**kwargs).execution_options(synchronize_session="fetch"))
        result=cls.get(db_session,id)
        return result if result else None
    @classmethod
    def delete(cls,db_session:DB_Session,id:str,*args, **kwargs)->BaseModelType:
        result=cls.get(db_session,id)
        db_session.execute(delete(cls).where(cls.id == id).execution_options(synchronize_session="fetch"))
        return result if result else None


class User(Base,BaseModel):
    pass
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.Text,nullable=False)
    absensi = relationship("Absensi")
    activity = relationship("Activity")

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def validate_user(cls,db_session:DB_Session,request):
        pass
        result=db_session.execute(select(cls).filter(cls.username==request.username)).first()
        if not result:
            raise LoginFailed("User tidak ditemukan")
        right=check_password_hash(result[0].password,request.password)
        if not right:
            raise LoginFailed("Password Salah")
        return result[0]

class Absensi(Base,BaseModel):
    __tablename__ = "absensi"
    id = db.Column(db.Integer, primary_key=True)
    check_in = db.Column(db.TIMESTAMP,nullable=True)
    check_out = db.Column(db.TIMESTAMP,nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="absensi")


    def __repr__(self):
        return '<Absensi %r>' % self.id

    @classmethod
    def get_by_check_in(cls,db_session:DB_Session,user_id:str,date:datetime.date)->BaseModelType:
        result=db_session.execute(select(cls).filter(and_(cls.user_id==user_id,cls.check_in>=date))).first()
        return result[0] if result else None

class Activity(Base,BaseModel):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text,nullable=False)
    description=db.Column(db.Text,nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="activity")

    def __repr__(self):
        return '<Activity %r>' % self.id

