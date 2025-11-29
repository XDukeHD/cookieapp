from src.bot.managers import SessionManager
from src.config import DEBUG_MODE


class AuthenticationManager:
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
        self.session = SessionManager()
    
    def is_authenticated(self):
        return self.session.is_logged_in()
    
    def check_authentication(self, command_name=None):
        if not self.is_authenticated():
            if DEBUG_MODE and command_name:
                print(f"Authentication failed for command: {command_name}")
            return False
        return True
    
    async def enforce_authentication(self, context, command_name=None):
        if not self.is_authenticated():
            message = "You are not logged in on this client."
            
            if isinstance(context, object) and hasattr(context, 'response'):
                await context.response.send_message(message, ephemeral=True)
            elif isinstance(context, object) and hasattr(context, 'send'):
                await context.send(message)
            
            return False
        return True
