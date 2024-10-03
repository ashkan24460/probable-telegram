from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
import datetime

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    wallet_address = Column(String)
    last_tap = Column(DateTime)
    ip_address = Column(String)
    boost_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)

def get_user(telegram_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    session.close()
    return user

def create_user(telegram_id, username, ip_address):
    session = Session()
    new_user = User(telegram_id=telegram_id, username=username, ip_address=ip_address)
    session.add(new_user)
    session.commit()
    session.close()

def update_user_points(telegram_id, points):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.points += points
        user.last_tap = datetime.datetime.utcnow()
        session.commit()
    session.close()

def record_transaction(user_id, amount, transaction_type):
    session = Session()
    new_transaction = Transaction(user_id=user_id, amount=amount, transaction_type=transaction_type)
    session.add(new_transaction)
    session.commit()
    session.close()

# Add more database functions as needed