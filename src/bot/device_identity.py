from src.utils.device import load_cookie


class DeviceIdentity:
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
        self.device_id = None
        self.device_name = None
        self.access_token = None
        self._load_identity()
    
    def _load_identity(self):
        cookie = load_cookie()
        if cookie:
            self.device_id = cookie.get('device_id')
            self.access_token = cookie.get('access_token')
    
    def get_device_name(self):
        if not self.device_name:
            import socket
            self.device_name = socket.gethostname()
        return self.device_name
    
    def get_device_id(self):
        return self.device_id
    
    def get_access_token(self):
        return self.access_token
    
    def update_token(self, new_token):
        self.access_token = new_token
