from sqlalchemy import Column, BigInteger, String

from findsbot.utils.dp_api.database import db


class Block(db.Model):
    __tablename__ = 'help_block'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)
