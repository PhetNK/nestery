from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'
    DeviceID = Column(Integer, primary_key=True, autoincrement=True)
    DeviceNumber = Column(String(50), nullable=False, unique=True)
    SerialNumber = Column(String(100), nullable=True)
    Hostname = Column(String(50), nullable=False)
    Model = Column(String(50))

    Sensors = relationship("Sensor", back_populates="Device")

class Sensor(Base):
    __tablename__ = 'sensor'
    SensorID = Column(Integer, primary_key=True, autoincrement=True)
    DeviceNumber = Column(String(50), ForeignKey('device.DeviceNumber'), nullable=False)
    Sensor = Column(String, nullable=False)
    SensorNumber = Column(String(50), nullable=True)
    SerialNumber = Column(String(100), nullable=True)
    Type = Column(String(50))
    Model = Column(String(50))
    Value = Column(Float)
    Unit = Column(String(20))
    Group = Column(String(50))
    Timestamp = Column(DateTime, default=datetime.utcnow)


# Connect to the database
db_name = "nestery"
user = "nestery_db"
passwd = "L0g!n"
hostname = "192.168.90.102"

engine = create_engine(f"postgresql://{user}:{passwd}@{hostname}:5432/{db_name}")

# Create all tables
try:
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")
