import dearpygui.dearpygui as dpg
from typing import Callable

def create_modal_window(
    title: str,
    content: Callable,
    width: int = 300,
    height: int = 125,
    tag: str = None
) -> None:
    """Creates a modal window with standard styling"""
    with dpg.window(
        label=title,
        modal=True,
        tag=tag or f"{title.lower()}_window",
        width=width,
        height=height,
        no_close=True
    ):
        content()

def show_error(message: str, width: int = 300) -> None:
    """Shows a standard error modal"""
    def error_content():
        dpg.add_text(message)
        dpg.add_spacer(height=20)
        dpg.add_button(
            label="OK",
            callback=lambda: dpg.delete_item("error_window"),
            width=width-20
        )
    
    create_modal_window("Error", error_content, width=width, tag="error_window")

def show_confirmation(
    message: str,
    on_confirm: Callable,
    on_cancel: Callable = None,
    width: int = 300
) -> None:
    """Shows a standard confirmation modal"""
    def confirm_content():
        dpg.add_text(message)
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Yes", callback=on_confirm)
            dpg.add_button(
                label="No",
                callback=on_cancel or (lambda: dpg.delete_item("confirm_window"))
            )
    
    create_modal_window("Confirm", confirm_content, width=width, tag="confirm_window")

def validate_coin_input(name: str, coin_id: str, avg_price: float, amount: float) -> None:
    """Validates coin input data"""
    if not all([name, coin_id, avg_price, amount]):
        raise ValueError("All fields except Target Prices are required")
    
    if avg_price <= 0:
        raise ValueError("Average price must be greater than 0")
    
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

def parse_targets(targets_text: str) -> list[float]:
    """Parses comma-separated target prices"""
    if not targets_text:
        return []
    
    try:
        targets = [float(t.strip()) for t in targets_text.split(",")]
        if any(t <= 0 for t in targets):
            raise ValueError("Target prices must be greater than 0")
        return targets
    except ValueError:
        raise ValueError("Invalid target price format. Use comma-separated numbers")

def format_currency(value: float) -> str:
    """Formats a value as USD currency"""
    return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    """Formats a value as percentage"""
    return f"{value:,.2f}%"

def get_profit_color(value: float) -> tuple[int, int, int]:
    """Returns RGB color tuple based on profit/loss"""
    return (0, 255, 0) if value >= 0 else (255, 0, 0)

def mask_sensitive_data(value: str, privacy_enabled: bool) -> str:
    """Masks sensitive data with asterisks when privacy mode is enabled"""
    return "****" if privacy_enabled else value

def verify_password(input_password: str) -> bool:
    """Verifies if the input password matches the configured password"""
    from config.settings import PRIVACY_MODE_PASSWORD
    return input_password == PRIVACY_MODE_PASSWORD