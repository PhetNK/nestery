from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from database.db_manager import DatabaseManager
from database.default_table import Device, Sensor, SensorReading


app = FastAPI()
session = DatabaseManager().get_session()

class HostModel(BaseModel):
    Hostname: str
    DeviceNumber: str
    SerialNumber: str
    Model: str

class SensorModel(BaseModel):
    Sensor: str
    SensorNumber: str
    SerialNumber: str
    Type: str
    Model: str
    Value: float
    Unit: str
    Group: str

class Payload(BaseModel):
    Host: list[HostModel]
    Sensors: list[SensorModel]

@app.post("/data")
def insert_data(payload: Payload):
    
    try:
        
        for host in payload.Host:
            existing_device = session.query(Device).filter_by(DeviceNumber=host.DeviceNumber).first()
            if not existing_device:
                new_device = Device(**host.dict())
                session.add(new_device)

        
        for sensor in payload.Sensors:
            existing_sensor = session.query(Sensor).filter_by(SensorNumber=sensor.SensorNumber).first()
            if not existing_sensor:
                new_sensor = Sensor(
                    SensorNumber=sensor.SensorNumber,
                    Sensor=sensor.Sensor,
                    SerialNumber=sensor.SerialNumber,
                    Type=sensor.Type,
                    Model=sensor.Model,
                    Unit=sensor.Unit,
                    Group=sensor.Group,
                    DeviceNumber=payload.Host[0].DeviceNumber
                )
                session.add(new_sensor)

        session.commit()

        for sensor in payload.Sensors:
            sensor_obj = session.query(Sensor).filter_by(SensorNumber=sensor.SensorNumber).first()
            if not sensor_obj:
                raise HTTPException(status_code=404, detail=f"Sensor {sensor.SensorNumber} not found")

            reading = SensorReading(
                SensorID=sensor_obj.SensorID,
                Value=sensor.Value,
                Timestamp=datetime.utcnow()
            )
            session.add(reading)

        session.commit()
        return {"message": "Data inserted successfully"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()