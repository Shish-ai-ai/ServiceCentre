from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, DATETIME,\
    SmallInteger, Numeric, Date, ForeignKey

Base = declarative_base()


class ClientDb(Base):
    __tablename__ = "client_db"
    __table_args__ = {"schema": "University"}
    ID = Column(BigInteger, primary_key=True)
    Client_name = Column(String(255))
    Car_number = Column(String(45))
    Car_mark = Column(String(45))
    Car_year = Column(SmallInteger)
    Phone_number = Column(String(45))


class ExecutorDb(Base):
    __tablename__ = "executor_db"
    __table_args__ = {"schema": "University"}
    ID = Column(BigInteger, primary_key=True)
    Address = Column(String(45))
    Phone_number = Column(Numeric)
    Executor_name = Column(String(255))
    Executor_birthday = Column(Date)
    Executor_post = Column(String(255))
    Salary = Column(Integer)
    Work_experience = Column(Integer)
    Seniority_allowance = Column(Integer)
    Schedule = Column(String)


class OrderServiceDb(Base):
    __tablename__ = "order-service_db"
    __table_args__ = {"schema": "University"}
    service_id = Column(BigInteger, ForeignKey('service_db.id'))
    order_id = Column(BigInteger, ForeignKey('order_db.id'))
    final_price = Column(Integer)
    id = Column(BigInteger, primary_key=True)


class OrderDb(Base):
    __tablename__ = "order_db"
    __table_args__ = {"schema": "University"}
    id = Column(BigInteger, primary_key=True)
    service_id = Column(BigInteger, ForeignKey('service_db.id'))
    order_id = Column(BigInteger, ForeignKey('order_db.id'))
    executor_id = Column(BigInteger, ForeignKey('executor_db.id'))
    order_time = Column(DATETIME)
    execution_time = Column(DATETIME)


class ServiceDb(Base):
    __tablename__ = "service_db"
    __table_args__ = {"schema": "University"}
    ID = Column(BigInteger, primary_key=True)
    Type = Column(String(45))
    Price = Column(Integer)
    Execution_time = Column(DATETIME)
    Items_to_change = Column(String)

