from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# тут для вас тоже ничего интересного нет
# здесь создается шлюз для подключения к базе данных
ENGINE = 'postgresql+psycopg2://user:iVj3zuVmXkzQyt1Oc3ph0KvWOms2swgg@dpg-chpptr67avjb90g5d9k0-a.oregon-postgres.render.com/brother_crypto_bot'
engine = create_engine(ENGINE)
DeclarativeBase = declarative_base()
DeclarativeBase.metadata.create_all(engine)