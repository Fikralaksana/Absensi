
import sqlalchemy as db
from sqlalchemy.orm import declarative_base

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
    password = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username