class SessionManager:
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
        self.current_device = None
        self.user_id = None
    
    def login(self, device_name, user_id):
        if self.current_device and self.current_device != device_name:
            self.logout()
        self.current_device = device_name
        self.user_id = user_id
    
    def logout(self):
        self.current_device = None
        self.user_id = None
    
    def get_current_device(self):
        return self.current_device
    
    def get_user_id(self):
        return self.user_id
    
    def is_logged_in(self):
        return self.current_device is not None
