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
        return bool(self.session.query(Users.user_id).filter(Users.user_id == user_id).all()[0][0])
