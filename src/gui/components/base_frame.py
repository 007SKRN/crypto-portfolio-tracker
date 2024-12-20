from src.models import Portfolio

from typing import Callable, Optional

class BaseFrame:
    def __init__(self, tag: str, portfolio: Portfolio, refresh_callback: Optional[Callable] = None):
        self.tag = tag
        self.portfolio = portfolio
        self.refresh_callback = refresh_callback
        self.setup_ui()

    def setup_ui(self):
        """Override this method to setup the frame's UI"""
        raise NotImplementedError

    def get_item_tag(self, item_name: str) -> str:
        """Generate a consistent tag for UI elements"""
        return f"{self.tag}_{item_name}"

    def refresh(self):
        """Call the refresh callback if it exists"""
        if self.refresh_callback:
            self.refresh_callback() 