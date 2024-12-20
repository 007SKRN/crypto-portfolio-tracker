from src.utils import show_error, validate_coin_input, parse_targets

import dearpygui.dearpygui as dpg

class AddCoinFrame:
    def __init__(self, tag, portfolio, refresh_callback):
        self.tag = tag
        self.portfolio = portfolio
        self.refresh_callback = refresh_callback
        self.setup_ui()

    def setup_ui(self):
        with dpg.group(tag=self.tag):
            with dpg.collapsing_header(label="Add New Coin", default_open=False):
                with dpg.group(horizontal=True):
                    with dpg.group():
                        dpg.add_input_text(
                            label="Coin Name",
                            tag=f"{self.tag}_name",
                            width=200
                        )
                        dpg.add_input_text(
                            label="CoinMarketCap ID",
                            tag=f"{self.tag}_id",
                            width=200
                        )
                        dpg.add_input_float(
                            label="Average Buy Price ($)",
                            tag=f"{self.tag}_price",
                            format="%.8g",
                            width=200
                        )

                    dpg.add_spacer(width=20)

                    with dpg.group():
                        dpg.add_input_float(
                            label="Amount",
                            tag=f"{self.tag}_amount",
                            format="%.8g",
                            width=200
                        )
                        dpg.add_input_text(
                            label="Target Prices ($)",
                            tag=f"{self.tag}_targets",
                            width=200
                        )

                dpg.add_spacer(height=10)

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Add Coin",
                        callback=self.add_coin,
                        tag=f"{self.tag}_add_button",
                        width=120
                    )
                    dpg.add_spacer(width=10)
                    dpg.add_button(
                        label="Clear Fields",
                        callback=self.clear_fields,
                        tag=f"{self.tag}_clear_button",
                        width=120
                    )

                self.setup_tooltips()

    def setup_tooltips(self):
        tooltips = {
            f"{self.tag}_name": "Enter the name of your cryptocurrency",
            f"{self.tag}_id": "Enter the CoinMarketCap ID (found in the URL of the coin's page)",
            f"{self.tag}_price": "Enter your average purchase price in USD",
            f"{self.tag}_amount": "Enter the amount of coins you own",
            f"{self.tag}_targets": "Enter target prices separated by commas (e.g., 45000,50000,55000)"
        }

        for item_tag, tooltip_text in tooltips.items():
            with dpg.tooltip(parent=item_tag):
                dpg.add_text(tooltip_text)

    def add_coin(self):
        try:
            name = dpg.get_value(f"{self.tag}_name")
            coin_id = dpg.get_value(f"{self.tag}_id")
            avg_price = dpg.get_value(f"{self.tag}_price")
            amount = dpg.get_value(f"{self.tag}_amount")
            targets_text = dpg.get_value(f"{self.tag}_targets")

            validate_coin_input(name, coin_id, avg_price, amount)
            targets = parse_targets(targets_text)

            self.portfolio.add_coin(name, coin_id, avg_price, amount, targets)
            self.refresh_callback()
            self.clear_fields()
        except ValueError as e:
            show_error(str(e))

    def clear_fields(self):
        dpg.set_value(f"{self.tag}_name", "")
        dpg.set_value(f"{self.tag}_id", "")
        dpg.set_value(f"{self.tag}_price", 0.0)
        dpg.set_value(f"{self.tag}_amount", 0.0)
        dpg.set_value(f"{self.tag}_targets", "")

    def show_error(self, message):
        with dpg.window(label="Error", modal=True, tag=f"{self.tag}_error_window"):
            dpg.add_text(message)
            dpg.add_button(
                label="OK",
                callback=lambda: dpg.delete_item(f"{self.tag}_error_window")
            )