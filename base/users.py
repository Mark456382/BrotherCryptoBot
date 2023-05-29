from sqlalchemy import Column, Integer
from base.settings import DeclarativeBase

class Users(DeclarativeBase):
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    tarif = Column('tarif', Integer)
    timer = Column('timer', Integer)