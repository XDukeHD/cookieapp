from src.utils.device import load_cookie


class PrefixManager:
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
        self.prefix = None
        self._load_prefix()
    
    def _load_prefix(self):
        cookie = load_cookie()
        if cookie and 'prefix' in cookie:
            self.prefix = cookie.get('prefix', '!')
        else:
            self.prefix = '!'
    
    def get_prefix(self):
        return self.prefix
