import requests
from src.config import API_URL, API_TIMEOUT, DECRYPT_KEY
from src.utils.device import load_cookie, save_cookie, get_cookie_file_path
from src.utils.encryption import decrypt_token


def fetch_and_decrypt_token(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(
            f'{API_URL}/api/getToken',
            headers=headers,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        
        api_response = response.json()
        
        if api_response.get('success'):
            encrypted_token = api_response.get('token')
            decrypted_token = decrypt_token(encrypted_token, DECRYPT_KEY)
            return True, decrypted_token
        else:
            return False, None
    
    except requests.exceptions.RequestException as e:
        return False, None


def refresh_token():
    cookie = load_cookie()
    
    if not cookie:
        return False
    
    access_token = cookie.get('access_token')
    
    if not access_token:
        return False
    
    success, decrypted_token = fetch_and_decrypt_token(access_token)
    
    if success:
        cookie['token'] = decrypted_token
        save_cookie(cookie)
        return True
    
    return False


def get_current_token():
    cookie = load_cookie()
    if cookie:
        return cookie.get('token')
    return None
