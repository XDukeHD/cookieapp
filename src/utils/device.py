import socket
import uuid
import json
import platform
import psutil
from pathlib import Path


def get_device_name():
    return socket.gethostname()


def get_device_id():
    mac_address = uuid.getnode()
    device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, socket.gethostname()))
    return device_id


def get_hardware_info():
    processor = platform.processor()
    machine = platform.machine()
    system = platform.system()
    
    cpu_count = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)
    
    memory = psutil.virtual_memory()
    total_memory_gb = memory.total / (1024**3)
    
    hardware_info = {
        'processor': processor,
        'machine': machine,
        'system': system,
        'cpu_cores': cpu_count,
        'cpu_logical_cores': cpu_count_logical,
        'total_memory_gb': round(total_memory_gb, 2)
    }
    
    return hardware_info


def get_device_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def get_device_location_from_ip(ip_address):
    import requests
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            location = {
                'city': data.get('city', ''),
                'region': data.get('region', ''),
                'country': data.get('country_name', ''),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
            return location
    except Exception:
        pass
    
    return {
        'city': 'Unknown',
        'region': 'Unknown',
        'country': 'Unknown',
        'latitude': None,
        'longitude': None
    }


def get_cookie_file_path():
    appdata_path = Path(os.getenv('APPDATA')) / 'CookieApp'
    appdata_path.mkdir(parents=True, exist_ok=True)
    return appdata_path / 'cookie.json'


def save_cookie(cookie_data):
    cookie_path = get_cookie_file_path()
    with open(cookie_path, 'w') as f:
        json.dump(cookie_data, f, indent=2)


def load_cookie():
    cookie_path = get_cookie_file_path()
    if cookie_path.exists():
        with open(cookie_path, 'r') as f:
            return json.load(f)
    return None


def is_device_registered():
    return load_cookie() is not None


import os
