from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'

    DeviceID = Column(Integer, primary_key=True, autoincrement=True)
    DeviceNumber = Column(String(50), nullable=False, unique=True)
    SerialNumber = Column(String(100), nullable=True)
    Hostname = Column(String(50), nullable=False)
    Model = Column(String(50), nullable=True)

    sensors = relationship("Sensor", back_populates="device", cascade="all, delete-orphan")

class Sensor(Base):
    __tablename__ = 'sensor'

    SensorID = Column(Integer, primary_key=True, autoincrement=True)
    SensorNumber = Column(String(50), nullable=False, unique=True)
    SerialNumber = Column(String(100), nullable=True)
    Sensor = Column(String(100), nullable=False)
    Type = Column(String(50), nullable=True)
    Model = Column(String(50), nullable=True)
    Unit = Column(String(20), nullable=True)
    Group = Column(String(50), nullable=True)
    DeviceNumber = Column(String(50), ForeignKey('device.DeviceNumber'), nullable=False)

    device = relationship("Device", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")

class SensorReading(Base):
    __tablename__ = 'sensor_reading'

    ReadingID = Column(Integer, primary_key=True, autoincrement=True)
    SensorID = Column(Integer, ForeignKey('sensor.SensorID'), nullable=False)
    Value = Column(Float, nullable=False)
    Timestamp = Column(DateTime, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="readings")