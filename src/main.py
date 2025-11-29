import sys
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.utils.logging_config import *
from src.config import (
    APP_NAME,
    APP_VERSION,
    DEBUG_MODE
)
from src.utils.device import is_device_registered, load_cookie
from src.modules.registration import register_device
from src.modules.token import refresh_token
from src.bot.handlers import DiscordConnectionHandler
from src.bot import DeviceIdentity


def initialize_device():
    if not is_device_registered():
        success, response = register_device()
        if success:
            if DEBUG_MODE:
                print(f"Device registered successfully: {response}")
            return True
        else:
            if DEBUG_MODE:
                print(f"Device registration failed: {response}")
            return False
    else:
        cookie = load_cookie()
        if DEBUG_MODE:
            print(f"Device already registered with token: {cookie.get('access_token')}")
        return True


def refresh_and_validate_token():
    success = refresh_token()
    if success:
        if DEBUG_MODE:
            print("Token refreshed and decrypted successfully")
        return True
    else:
        print("Failed to refresh token")
        return False


async def start_bot():
    handler = DiscordConnectionHandler()
    await handler.setup()
    await handler.run()


def main():
    if DEBUG_MODE:
        print(f"{APP_NAME} v{APP_VERSION}")
    
    if not initialize_device():
        print("Failed to initialize device")
        sys.exit(1)
    
    if not refresh_and_validate_token():
        sys.exit(1)
    
    device_identity = DeviceIdentity()
    device_name = device_identity.get_device_name()
    if DEBUG_MODE:
        print(f"Starting child bot for device: {device_name}")
    
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        if DEBUG_MODE:
            print("Application terminated by user")
        sys.exit(0)
    except Exception as e:
        if DEBUG_MODE:
            print(f"Application error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
