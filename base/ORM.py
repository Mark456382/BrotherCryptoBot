from base.settings import *
from base.users import Users
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

class BrotherCryptoBot:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session(autoflush=False, bind=engine)

    def add_user(self, user_id):
        try:
            post = Users(user_id=user_id)
            self.session.add(post)
            self.session.commit()
            return self.session.close()
        except BaseException as e:
            print(f'Что то пошло не так\nОшибка: {e}')
        finally:
            self.session.close()

    def check_user(self, user_id):
        return self.session.query(Users.user_id).filter(Users.user_id == user_id).all()

    def set_tarif(self, user_id, tarif, time):
        obj =  self.session.query(Users).filter(Users.user_id == user_id).first()
        obj.tarif = tarif
        obj.timer = time
        self.session.commit()

    def get_tarif(self, user_id):
        return self.session.query(Users.tarif).filter(Users.user_id == user_id).all()[0][0]
    
    def get_time(self, user_id):
        return self.session.query(Users.timer).filter(Users.user_id == user_id).all()[0][0]
    
    def get_all_user_id(self):
        post = self.session.query(Users.user_id, Users.timer).all()
        users = []
        for i in post:
            users.append([i[0], i[1]])
        return users
    
    def set_time(self, user_id, time):
        obj =  self.session.query(Users).filter(Users.user_id == user_id).first()
        obj.timer = time
        self.session.commit()

    def users_with_tarif(self):
        return self.session.query(Users.user_id).filter(Users.tarif != None).all()

db = BrotherCryptoBot()
print(db.get_all_user_id())