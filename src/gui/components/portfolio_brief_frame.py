from src.utils import PrivacyManager, format_currency, format_percentage, get_profit_color, mask_sensitive_data

import dearpygui.dearpygui as dpg

class PortfolioBriefFrame:
    def __init__(self, tag, portfolio, portfolio_frame=None):
        self.tag = tag
        self.portfolio = portfolio
        self.portfolio_frame = portfolio_frame
        self.privacy_manager = PrivacyManager()
        self.setup_ui()
        self.update_brief()

    def setup_ui(self):
        with dpg.group(tag=self.tag):
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            with dpg.group(horizontal=True):
                dpg.add_text("Privacy Mode:")
                dpg.add_button(
                    label="Toggle Privacy",
                    callback=self.toggle_privacy,
                    tag=f"{self.tag}_privacy_toggle"
                )
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text("Total Investment")
                    dpg.add_text("$0.00", tag=f"{self.tag}_total_investment")

                dpg.add_spacer(width=20)

                with dpg.group():
                    dpg.add_text("Current Value")
                    dpg.add_text("$0.00", tag=f"{self.tag}_current_value")

                dpg.add_spacer(width=20)

                with dpg.group():
                    dpg.add_text("Total Profit/Loss")
                    dpg.add_text("$0.00 (0.00%)", tag=f"{self.tag}_total_profit")

            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)

    def toggle_privacy(self):
        if self.privacy_manager.is_privacy_enabled():
            self.show_password_modal()
        else:
            self.privacy_manager.toggle_privacy()
            self.update_brief()
            self.portfolio_frame.update_portfolio_view()

    def show_password_modal(self):
        with dpg.window(label="Enter Password", modal=True, tag="password_modal", width=300, height=180):
            dpg.add_text("Enter password to disable privacy mode:")
            dpg.add_spacer(height=10)
            dpg.add_input_text(
                tag="password_input",
                password=True,
                width=280
            )
            dpg.add_text(
                "Incorrect password!",
                tag="password_error_text",
                color=(255, 0, 0),
                show=False
            )
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Submit",
                    callback=self.verify_password,
                    width=135
                )
                dpg.add_button(
                    label="Cancel",
                    callback=lambda: dpg.delete_item("password_modal"),
                    width=135
                )

    def verify_password(self):
        password = dpg.get_value("password_input")
        if self.privacy_manager.toggle_privacy(password):
            dpg.delete_item("password_modal")
            self.update_brief()
            if self.portfolio_frame:
                self.portfolio_frame.update_portfolio_view()
        else:
            dpg.set_value("password_input", "")
            dpg.configure_item("password_error_text", show=True)

    def update_brief(self):
        portfolio_data = self.portfolio.get_portfolio_data()
        privacy_enabled = self.privacy_manager.is_privacy_enabled()

        total_investment = sum(coin["investment"] for coin in portfolio_data)
        current_value = sum(coin["current_value"] for coin in portfolio_data)
        total_profit = current_value - total_investment
        profit_percentage = (total_profit / total_investment * 100) if total_investment > 0 else 0

        dpg.set_value(
            f"{self.tag}_total_investment",
            mask_sensitive_data(format_currency(total_investment), privacy_enabled)
        )
        dpg.set_value(
            f"{self.tag}_current_value",
            mask_sensitive_data(format_currency(current_value), privacy_enabled)
        )
        dpg.set_value(
            f"{self.tag}_total_profit",
            f"{mask_sensitive_data(format_currency(total_profit), privacy_enabled)} ({format_percentage(profit_percentage)})"
        )
        dpg.configure_item(
            f"{self.tag}_total_profit",
            color=get_profit_color(total_profit)
        )
