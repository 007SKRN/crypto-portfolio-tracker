from src.gui.components import PortfolioBriefFrame, PortfolioFrame, AddCoinFrame
from config.settings import REFRESH_INTERVAL
from src.models import Portfolio
from src.utils import logger

import dearpygui.dearpygui as dpg
import webbrowser
import time

class App:
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(title="Crypto Portfolio Tracker",
                            width=1200,
                            height=800,
                            small_icon="assets/icon.ico",
                            large_icon="assets/icon.ico")
        
        self.portfolio = Portfolio()
        self.last_refresh = 0

        with dpg.window(tag="main_window", label="Crypto Portfolio", no_scrollbar=True):
            self.add_coin_frame = AddCoinFrame("add_coin_frame", self.portfolio, self.refresh_portfolio)
            self.portfolio_brief_frame = PortfolioBriefFrame("portfolio_brief_frame", self.portfolio)
            self.portfolio_frame = PortfolioFrame("portfolio_frame", self.portfolio, self.portfolio_brief_frame)
            self.portfolio_brief_frame.portfolio_frame = self.portfolio_frame
            self.portfolio_frame.portfolio_brief_frame = self.portfolio_brief_frame
            
            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
            
            self.include_credits()

        dpg.setup_dearpygui()
        dpg.set_primary_window("main_window", True)
        dpg.show_viewport()

    def refresh_portfolio(self):
        self.portfolio_frame.update_portfolio_view()
        self.portfolio_brief_frame.update_brief()
        self.last_refresh = time.time()
        logger.info("Portfolio refreshed")

    def check_refresh(self):
        current_time = time.time()
        if current_time - self.last_refresh >= REFRESH_INTERVAL:
            self.refresh_portfolio()

    def include_credits(self):
        with dpg.group(horizontal=True):
            dpg.add_text("Built by: ")
            dpg.add_button(
                label="007SKRN",
                callback=lambda: webbrowser.open("https://github.com/007SKRN"),
                small=True
            )
            
            dpg.add_spacer(width=5)
            dpg.add_text("|")
            dpg.add_spacer(width=5)
            
            dpg.add_text("Repository: ")
            dpg.add_button(
                label="crypto-portfolio-tracker",
                callback=lambda: webbrowser.open("https://github.com/007SKRN/crypto-portfolio-tracker"),
                small=True
            )
            
            dpg.add_spacer(width=5)
            dpg.add_text("|")
            dpg.add_spacer(width=5)

            dpg.add_text("Version: ")
            dpg.add_text("1.0.0")

    def run(self):
        while dpg.is_dearpygui_running():
            self.check_refresh()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()