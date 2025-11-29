import requests
import json
from src.config import API_URL, API_TIMEOUT
from src.utils.device import (
    get_device_name,
    get_device_id,
    get_hardware_info,
    get_device_ip,
    get_device_location_from_ip,
    save_cookie
)


def register_device():
    device_name = get_device_name()
    device_id = get_device_id()
    device_hardware = get_hardware_info()
    device_ip = get_device_ip()
    device_location = get_device_location_from_ip(device_ip)
    
    payload = {
        'device_name': device_name,
        'device_id': device_id,
        'device_hardware': device_hardware,
        'device_actualIP': device_ip,
        'device_location': device_location
    }
    
    try:
        response = requests.post(
            f'{API_URL}/api/deviceRegister',
            json=payload,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        
        api_response = response.json()
        
        if api_response.get('success'):
            cookie_data = {
                'created_at': api_response.get('created_at'),
                'access_token': api_response.get('access_token'),
                'device_id': api_response.get('device_id')
            }
            save_cookie(cookie_data)
            return True, api_response
        else:
            return False, api_response
    
    except requests.exceptions.RequestException as e:
        return False, {'error': str(e)}
