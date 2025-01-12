import dearpygui.dearpygui as dpg

class EditCoinFrame:
    def __init__(self, portfolio, db_id, refresh_callback):
        self.portfolio = portfolio
        self.db_id = db_id
        self.coin_data = portfolio.get_coin(db_id)
        self.refresh_callback = refresh_callback
        self.show()

    def show(self):
        with dpg.window(
            label=f"Edit {self.coin_data['name']}", 
            modal=True, 
            tag="edit_window",
            width=500,
            height=200,
            pos=[dpg.get_viewport_width() // 2 - 200, dpg.get_viewport_height() // 2 - 150]
        ):
            with dpg.group():
                dpg.add_input_text(
                    label="Name",
                    default_value=self.coin_data["name"],
                    tag="edit_name",
                    width=350
                )
                dpg.add_input_text(
                    label="CoinMarketCap ID",
                    default_value=self.coin_data["id"],
                    tag="edit_id",
                    width=350
                )
                dpg.add_input_float(
                    label="Average Price ($)",
                    default_value=self.coin_data["avg_price"],
                    tag="edit_price",
                    width=350,
                    format="%.8g"
                )
                dpg.add_input_float(
                    label="Amount",
                    default_value=self.coin_data["amount"],
                    tag="edit_amount",
                    width=350,
                    format="%.8g"
                )
                dpg.add_input_text(
                    label="Target Prices ($)",
                    default_value=",".join(map(str, self.coin_data["targets"])),
                    tag="edit_targets",
                    width=350
                )

                dpg.add_spacer(height=20)

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Save",
                        callback=self.save_changes,
                        width=170
                    )
                    dpg.add_spacer(width=10)
                    dpg.add_button(
                        label="Cancel",
                        callback=lambda: dpg.delete_item("edit_window"),
                        width=170
                    )

    def save_changes(self):
        try:
            name = dpg.get_value("edit_name")
            coin_id = dpg.get_value("edit_id")
            avg_price = dpg.get_value("edit_price")
            amount = dpg.get_value("edit_amount")
            targets_text = dpg.get_value("edit_targets")

            if not all([name, coin_id, avg_price, amount]):
                raise ValueError("All fields except Target Prices are required")

            # Targets are optional
            targets = []
            if targets_text:
                targets = [float(t.strip()) for t in targets_text.split(",")]

            self.portfolio.update_coin(self.db_id, name, coin_id, avg_price, amount, targets)

            self.refresh_callback()
            dpg.delete_item("edit_window")
        except ValueError as e:
            self.show_error("Invalid input. Please check your values.")

    def show_error(self, message):
        with dpg.window(label="Error", modal=True, tag="error_window", width=300, height=100):
            dpg.add_text(message)
            dpg.add_spacer(height=20)
            dpg.add_button(
                label="OK",
                callback=lambda: dpg.delete_item("error_window"),
                width=280
            )
