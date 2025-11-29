from src.modules.token import refresh_token, get_current_token


class TokenManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
    
    def get_discord_token(self):
        return get_current_token()
    
    def refresh_discord_token(self):
        return refresh_token()
