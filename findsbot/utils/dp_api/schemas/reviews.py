from sqlalchemy import Column, BigInteger, String, DateTime

from findsbot.utils.dp_api.database import db


class Reviews(db.Model):
    __tablename__ = 'finds_reviews'
    id = Column(BigInteger, primary_key=True)
    author_id = Column(BigInteger)
    caption = Column(String(3072))
    posted = Column(DateTime(timezone=True), default=db.func.now())
