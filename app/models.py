"""
Pydantic модели для валидации входящих данных
"""
from pydantic import BaseModel
from typing import Optional


class DeviceStatusEvent(BaseModel):
    """Модель события статуса устройства"""
    device_id: str
    name: Optional[str] = None
    battery: int
    signal_strength: int
    network_type: str
    internet: str
    timestamp: str
    type: str = "device_status"


class SMSEvent(BaseModel):
    """Модель события SMS"""
    device_id: str
    sender: str
    message: str
    timestamp: str
    type: str = "sms"


class BootCompletedEvent(BaseModel):
    """Модель события перезагрузки устройства"""
    device_id: str
    name: Optional[str] = None
    timestamp: str
    type: str = "boot_completed"


class GenericEvent(BaseModel):
    """Общая модель для любого события"""
    device_id: str
    type: str
    timestamp: str

