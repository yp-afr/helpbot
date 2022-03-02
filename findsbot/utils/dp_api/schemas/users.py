from sqlalchemy import Column, BigInteger, DateTime

from findsbot.utils.dp_api.database import db


class User(db.Model):
    __tablename__ = 'finds_users'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    date = Column(DateTime(True), server_default=db.func.now())
