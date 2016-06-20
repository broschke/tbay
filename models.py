from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, desc


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    
    bids = relationship("Bid", backref="item")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    items = relationship("Item", backref="user")
    
    bids = relationship("Bid", backref="user")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    
    item_id = Column(Integer, ForeignKey("items.id"),nullable=False)
    
#all classes before this line
Base.metadata.create_all(engine)

bob = User(username='Bob Smith',password='1234')
jessica = User(username='Jessica Jones', password='strong')
mick = User(username='Mickey Mantle', password='bat')

baseball = Item(name='baseball')
baseball.user = mick
session.add_all([bob, jessica, mick, baseball])
session.commit()

result = session.query(User).filter(User.username=='Mickey Mantle').first()

print(result)
print(result.items)

bid1 = Bid(price=5,user=bob,item=baseball)
bid2 = Bid(price=6,user=jessica,item=baseball)

highest_bid = session.query(Bid).order_by(desc(Bid.price)).first()

print(highest_bid.price)
print(highest_bid.user.username)

