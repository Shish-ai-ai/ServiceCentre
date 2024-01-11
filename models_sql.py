from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, BigInteger, DATETIME, SmallInteger, Numeric, Date, ForeignKey

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
    # orders = relationship("OrderDb", back_populates="client", foreign_keys="[OrderDb.Client_ID]")


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
    # orders = relationship("OrderDb", back_populates="executor", foreign_keys="[OrderDb.Executor_ID]")


class OrderDb(Base):
    __tablename__ = "order_db"
    __table_args__ = {"schema": "University"}
    __bind_key__ = "University"
    ID = Column(BigInteger, primary_key=True)
    Service_ID = Column(ForeignKey('service_db.ID'))
    Client_ID = Column(ForeignKey('client_db.ID'))
    Executor_ID = Column(ForeignKey('executor_db.ID'))
    Order_time = Column(DATETIME)
    execution_time = Column(DATETIME)
    # client = relationship("ClientDb", back_populates="orders", foreign_keys=[Client_ID])
    # service = relationship("ServiceDb", back_populates="orders", foreign_keys=[Service_ID])
    # executor = relationship("ExecutorDb", back_populates="orders", foreign_keys=[Executor_ID])


class ServiceDb(Base):
    __tablename__ = "service_db"
    __table_args__ = {"schema": "University"}
    __bind_key__ = "University"
    ID = Column(BigInteger, primary_key=True)
    Type = Column(String(45))
    Price = Column(Integer)
    Execution_time = Column(DATETIME)
    Items_to_change = Column(String)
    # orders = relationship("OrderDb", back_populates="service", foreign_keys="OrderDb.Service_ID")


class OrderServiceDb(Base):
    __tablename__ = "order_service_db"
    __table_args__ = {"schema": "University"}
    __bind_key__ = "University"
    service_ID = Column(ForeignKey('University.service_db.ID'))
    order_ID = Column(ForeignKey('University.order_db.ID'))
    final_price = Column(Integer)
    ID = Column(BigInteger, primary_key=True)
    service = relationship("ServiceDb")
