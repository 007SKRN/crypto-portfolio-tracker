from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///crypto_portfolio.db')
Session = sessionmaker(bind=engine)

class CoinModel(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    coin_id = Column(String, nullable=False)
    avg_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    targets = Column(JSON)

Base.metadata.create_all(engine)