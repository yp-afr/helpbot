from sqlalchemy import Column, BigInteger, String, DateTime

from findsbot.utils.dp_api.database import db


class RecordsUsers(db.Model):
    __tablename__ = "help_records_users"

    id = Column(BigInteger, primary_key=True)
    record_id = Column(BigInteger)
    chat_id = Column(BigInteger)
    message_id = Column(BigInteger)

