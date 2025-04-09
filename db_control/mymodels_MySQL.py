from sqlalchemy import Integer, String, DECIMAL, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declarative_base
from sqlalchemy import Time
from datetime import time
Base = declarative_base()

class Base(DeclarativeBase):
    pass

class Customers(Base):
    __tablename__ = 'customers'
    customer_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))

# add nakano start
class profile(Base):
    __tablename__ = 'profile'
    dog_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    regist_date: Mapped[str] = mapped_column(String(10))
    dog_code: Mapped[int] = mapped_column(Integer)
    dog_name: Mapped[str] = mapped_column(String(200))
    birthday: Mapped[str] = mapped_column(String(10))
    weight: Mapped[float] = mapped_column(DECIMAL(3, 1))
    height: Mapped[float] = mapped_column(DECIMAL(3, 1))
    photo: Mapped[bytes] = mapped_column(LargeBinary)
    memo: Mapped[str] = mapped_column(String(200))
    
class history_tbl(Base):
    __tablename__ = 'history_tbl'
    user_id: Mapped[int] = mapped_column(Integer)
    dog_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(String(10))
    training_stroll: Mapped[int] = mapped_column(Integer)
    sound_id: Mapped[int] = mapped_column(Integer)
    mood: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    
class music_tbl(Base):
    __tablename__ = 'music_tbl'
    sound_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    dog_id: Mapped[int] = mapped_column(Integer)
    music_type_code: Mapped[int] = mapped_column(Integer)
    music_data: Mapped[bytes] = mapped_column(LargeBinary)
    title: Mapped[str] = mapped_column(String(200))
    duration: Mapped[time] = mapped_column(Time)
    
# add nakano end

class Items(Base):
    __tablename__ = 'items'
    item_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    item_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)


class Purchases(Base):
    __tablename__ = 'purchases'
    purchase_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(10))
    purchase_date: Mapped[str] = mapped_column(String(10))


class PurchaseDetails(Base):
    __tablename__ = 'purchase_details'
    detail_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    purchase_id: Mapped[str] = mapped_column(String(10))
    item_id: Mapped[str] = mapped_column(String(10))
    quantity: Mapped[int] = mapped_column(Integer)
