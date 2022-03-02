from sqlalchemy import Column, BigInteger, String

from findsbot.utils.dp_api.database import db


class Contact(db.Model):
    __tablename__ = 'help_contacts'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)
