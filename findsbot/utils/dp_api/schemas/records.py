from sqlalchemy import Column, BigInteger, String, DateTime

from findsbot.utils.dp_api.database import db


class Records(db.Model):
    __tablename__ = "help_records"

    id = Column(BigInteger, primary_key=True)
    author_id = Column(BigInteger)
    author_username = Column(String(64))
    photo = Column(String(1024))
    caption = Column(String(3072))
    type = Column(String(64))
    category = db.Column(db.String(64))
    posted = Column(DateTime(timezone=True), default=db.func.now())



