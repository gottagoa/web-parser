from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, Text, DateTime, DECIMAL, Float
from db import get_session

BASE=declarative_base()



class PostManager():

    def  __init__(self):
        self.model = HousePost
        self.session = get_session()

    
    def insert_data(self, data, link):
        self.session.add(
            self.model(
                title=data["title"],
                address=data["address"],
                phone_number=data["phone_number"],
                price_som=data["price_som"],
                price_dollar=data["price_dollar"],
                lon=data["lon"],
                lat=data["lat"],
                description=data["description"],
                link=link,
            )
        )
        self.session.commit()
        self.session.close()
    
    def check_link(self, link):
        from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
        try:    
            r=self.session.query(self.model).filter_by(link=link).one()
            return True # Возвращает True если в базе есть уже эта запись
        except NoResultFound:
            return False # Возвращает False, если в базе отсутствует эта ссылка.
        except MultipleResultsFound:
            return True



class HousePost(BASE):
    __tablename__ = "post"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    price_som = Column(DECIMAL(10,2), nullable=False)
    price_dollar = Column(DECIMAL(10,2), nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    link = Column(String(2048))





















