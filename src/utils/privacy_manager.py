from config.settings import PRIVACY_MODE

class PrivacyManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.privacy_enabled = PRIVACY_MODE
        return cls._instance
    
    def toggle_privacy(self, password: str = None) -> bool:
        from src.utils import verify_password
        
        if self.privacy_enabled and password is not None:
            if verify_password(password):
                self.privacy_enabled = False
                return True
            return False
        else:
            self.privacy_enabled = True
            return True
    
    def is_privacy_enabled(self) -> bool:
        return self.privacy_enabled
