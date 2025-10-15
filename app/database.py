"""
Модуль для работы с базой данных SQLite
Содержит функции для создания таблиц и работы с данными
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


DATABASE_NAME = os.getenv('DATABASE_PATH', 'devices.db')


def get_connection():
    """Создать соединение с базой данных"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
    return conn


def init_database():
    """Инициализация базы данных и создание таблиц"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица устройств
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            name TEXT,
            battery INTEGER,
            signal_strength INTEGER,
            network_type TEXT,
            internet TEXT,
            last_seen TEXT,
            online BOOLEAN DEFAULT 0
        )
    """)
    
    # Таблица событий
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            type TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    """)
    
    # Таблица SMS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sms_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            sender TEXT,
            message TEXT,
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    """)
    
    # Таблица привязок устройств к Telegram чатам
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_chat_bindings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(device_id, chat_id),
            FOREIGN KEY (device_id) REFERENCES devices (id)
        )
    """)
    
    conn.commit()
    conn.close()


def save_event(device_id: str, event_type: str, timestamp: str, data: dict):
    """Сохранить событие в таблицу events"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO events (device_id, type, timestamp, data)
        VALUES (?, ?, ?, ?)
    """, (device_id, event_type, timestamp, json.dumps(data, ensure_ascii=False)))
    
    conn.commit()
    conn.close()


def update_device(device_id: str, data: dict):
    """Обновить или создать запись устройства"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Проверяем, существует ли устройство
    cursor.execute("SELECT id FROM devices WHERE id = ?", (device_id,))
    exists = cursor.fetchone()
    
    timestamp = data.get('timestamp', datetime.now().isoformat())
    
    if exists:
        # Обновляем существующее устройство
        update_fields = []
        values = []
        
        if 'name' in data:
            update_fields.append("name = ?")
            values.append(data['name'])
        if 'battery' in data:
            update_fields.append("battery = ?")
            values.append(data['battery'])
        if 'signal_strength' in data:
            update_fields.append("signal_strength = ?")
            values.append(data['signal_strength'])
        if 'network_type' in data:
            update_fields.append("network_type = ?")
            values.append(data['network_type'])
        if 'internet' in data:
            update_fields.append("internet = ?")
            values.append(data['internet'])
        
        update_fields.append("last_seen = ?")
        values.append(timestamp)
        
        values.append(device_id)
        
        cursor.execute(f"""
            UPDATE devices 
            SET {', '.join(update_fields)}
            WHERE id = ?
        """, values)
    else:
        # Создаем новое устройство
        cursor.execute("""
            INSERT INTO devices (id, name, battery, signal_strength, network_type, internet, last_seen, online)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            device_id,
            data.get('name', f'Device {device_id}'),
            data.get('battery', 0),
            data.get('signal_strength', 0),
            data.get('network_type', 'Unknown'),
            data.get('internet', 'Unknown'),
            timestamp
        ))
    
    conn.commit()
    conn.close()


def save_sms(device_id: str, timestamp: str, sender: str, message: str):
    """Сохранить SMS в таблицу sms_logs"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO sms_logs (device_id, timestamp, sender, message)
        VALUES (?, ?, ?, ?)
    """, (device_id, timestamp, sender, message))
    
    conn.commit()
    conn.close()


def get_all_devices() -> List[Dict]:
    """Получить список всех устройств с автоопределением online статуса"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()
    
    devices = []
    now = datetime.now()
    
    for row in rows:
        device = dict(row)
        
        # Автоопределение online статуса (последнее обновление менее 35 минут назад)
        if device['last_seen']:
            try:
                # Пробуем разные форматы даты
                last_seen = None
                
                # Формат: "14.10.2025 12:00:00"
                try:
                    last_seen = datetime.strptime(device['last_seen'], "%d.%m.%Y %H:%M:%S")
                except:
                    pass
                
                # Формат ISO: "2025-10-14T12:00:00"
                if not last_seen:
                    try:
                        last_seen = datetime.fromisoformat(device['last_seen'])
                    except:
                        pass
                
                if last_seen:
                    diff_minutes = (now - last_seen).total_seconds() / 60
                    device['online'] = diff_minutes < 20
                else:
                    device['online'] = False
            except Exception as e:
                print(f"⚠️ Ошибка парсинга даты для устройства {device.get('id')}: {e}")
                device['online'] = False
        else:
            device['online'] = False
        
        devices.append(device)
    
    conn.close()
    return devices


def get_device_by_id(device_id: str) -> Optional[Dict]:
    """Получить информацию о конкретном устройстве"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    device = dict(row)
    
    # Автоопределение online статуса
    if device['last_seen']:
        try:
            # Пробуем разные форматы даты
            last_seen = None
            
            # Формат: "14.10.2025 12:00:00"
            try:
                last_seen = datetime.strptime(device['last_seen'], "%d.%m.%Y %H:%M:%S")
            except:
                pass
            
            # Формат ISO: "2025-10-14T12:00:00"
            if not last_seen:
                try:
                    last_seen = datetime.fromisoformat(device['last_seen'])
                except:
                    pass
            
            if last_seen:
                diff_minutes = (datetime.now() - last_seen).total_seconds() / 60
                device['online'] = diff_minutes < 20
            else:
                device['online'] = False
        except Exception as e:
            print(f"⚠️ Ошибка парсинга даты для устройства {device_id}: {e}")
            device['online'] = False
    else:
        device['online'] = False
    
    conn.close()
    return device


def get_device_sms(device_id: str) -> List[Dict]:
    """Получить все SMS для конкретного устройства"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM sms_logs 
        WHERE device_id = ? 
        ORDER BY timestamp DESC
    """, (device_id,))
    
    rows = cursor.fetchall()
    sms_list = [dict(row) for row in rows]
    
    conn.close()
    return sms_list


# ===== Функции для работы с привязками устройств к Telegram чатам =====

def add_device_binding(device_id: str, chat_id: int) -> bool:
    """Привязать устройство к Telegram чату"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO device_chat_bindings (device_id, chat_id, created_at)
            VALUES (?, ?, ?)
        """, (device_id, chat_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Привязка уже существует
        conn.close()
        return False


def remove_device_binding(device_id: str, chat_id: int) -> bool:
    """Отвязать устройство от Telegram чата"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM device_chat_bindings 
        WHERE device_id = ? AND chat_id = ?
    """, (device_id, chat_id))
    
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_chat_bindings(chat_id: int) -> List[str]:
    """Получить список устройств, привязанных к чату"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT device_id FROM device_chat_bindings 
        WHERE chat_id = ?
    """, (chat_id,))
    
    rows = cursor.fetchall()
    device_ids = [row['device_id'] for row in rows]
    
    conn.close()
    return device_ids


def get_device_chats(device_id: str) -> List[int]:
    """Получить список чатов, к которым привязано устройство"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT chat_id FROM device_chat_bindings 
        WHERE device_id = ?
    """, (device_id,))
    
    rows = cursor.fetchall()
    chat_ids = [row['chat_id'] for row in rows]
    
    conn.close()
    return chat_ids

