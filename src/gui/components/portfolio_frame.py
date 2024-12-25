from src.utils import mask_sensitive_data, show_confirmation, show_error, PrivacyManager
from src.gui.components import EditCoinFrame
from src.models import TableColumns

import dearpygui.dearpygui as dpg

class PortfolioFrame:
    def __init__(self, tag, portfolio, portfolio_brief_frame=None):
        self.tag = tag
        self.portfolio = portfolio
        self.portfolio_brief_frame = portfolio_brief_frame
        self.privacy_manager = PrivacyManager()
        self.column_ids = None
        self.current_sort = None
        self.setup_ui()
        self.current_sort = (self.column_ids["profit"], -1)
        self.update_portfolio_view()

    def setup_ui(self):
        with dpg.group(tag=self.tag):
            with dpg.group(horizontal=True):
                dpg.add_text("Portfolio Overview", tag=f"{self.tag}_title")
                dpg.add_spacer(width=10)
                dpg.add_button(label="Refresh", callback=self.update_portfolio_view)

            with dpg.table(header_row=True, resizable=True,
                           policy=dpg.mvTable_SizingStretchProp,
                           borders_innerH=True, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True,
                           sortable=True,
                           callback=self.sort_callback,
                           tag=f"{self.tag}_table"):
                
                self.column_ids = {
                    "name": dpg.add_table_column(label=TableColumns.NAME.label, init_width_or_weight=TableColumns.NAME.width),
                    "current_price": dpg.add_table_column(label=TableColumns.CURRENT_PRICE.label, init_width_or_weight=TableColumns.CURRENT_PRICE.width),
                    "avg_price": dpg.add_table_column(label=TableColumns.AVG_PRICE.label, init_width_or_weight=TableColumns.AVG_PRICE.width),
                    "amount": dpg.add_table_column(label=TableColumns.AMOUNT.label, init_width_or_weight=TableColumns.AMOUNT.width),
                    "investment": dpg.add_table_column(label=TableColumns.INVESTMENT.label, init_width_or_weight=TableColumns.INVESTMENT.width),
                    "current_value": dpg.add_table_column(label=TableColumns.CURRENT_VALUE.label, init_width_or_weight=TableColumns.CURRENT_VALUE.width),
                    "profit": dpg.add_table_column(label=TableColumns.PROFIT.label, init_width_or_weight=TableColumns.PROFIT.width, default_sort=True, prefer_sort_descending=True),
                    "portfolio_percentage": dpg.add_table_column(label=TableColumns.PORTFOLIO_PERCENTAGE.label, init_width_or_weight=TableColumns.PORTFOLIO_PERCENTAGE.width),
                    "changes": dpg.add_table_column(label=TableColumns.CHANGES.label, init_width_or_weight=TableColumns.CHANGES.width),
                    "volume": dpg.add_table_column(label=TableColumns.VOLUME.label, init_width_or_weight=TableColumns.VOLUME.width),
                    "targets": dpg.add_table_column(label=TableColumns.TARGETS.label, init_width_or_weight=TableColumns.TARGETS.width, no_sort=True),
                    "actions": dpg.add_table_column(label=TableColumns.ACTIONS.label, init_width_or_weight=TableColumns.ACTIONS.width, no_sort=True)
                }

    def update_portfolio_view(self):
        self.sort_callback(None, None)

    def sort_callback(self, sender, sort_specs):
        if sort_specs is None and not self.current_sort:
            return

        if sort_specs:
            self.current_sort = (sort_specs[0][0], sort_specs[0][1])
        
        rows = self.portfolio.get_portfolio_data()
        column_id = self.current_sort[0]
        reverse = self.current_sort[1] < 0

        sort_keys = {
            self.column_ids["name"]: lambda x: x["name"],
            self.column_ids["current_price"]: lambda x: x["current_price"],
            self.column_ids["avg_price"]: lambda x: x["avg_price"],
            self.column_ids["amount"]: lambda x: float(x["amount"]),
            self.column_ids["investment"]: lambda x: x["investment"],
            self.column_ids["current_value"]: lambda x: x["current_value"],
            self.column_ids["profit"]: lambda x: x["profit"],
            self.column_ids["portfolio_percentage"]: lambda x: x["portfolio_percentage"],
            self.column_ids["changes"]: lambda x: x["changes"]["24h"],
            self.column_ids["volume"]: lambda x: x["volume"]["change_24h"],
            self.column_ids["targets"]: lambda x: len(x["targets"]),
        }

        if column_id in sort_keys:
            rows.sort(key=sort_keys[column_id], reverse=reverse)
            self.update_table_with_data(rows)

    def update_table_with_data(self, rows):
        privacy_enabled = self.privacy_manager.is_privacy_enabled()
        
        table_tag = f"{self.tag}_table"
        dpg.delete_item(table_tag, children_only=True, slot=1)

        for coin_data in rows:
            with dpg.table_row(parent=table_tag):
                dpg.add_text(coin_data["name"])
                dpg.add_text(TableColumns.CURRENT_PRICE.format.format(coin_data['current_price']))
                dpg.add_text(TableColumns.AVG_PRICE.format.format(coin_data['avg_price']))
                dpg.add_text(mask_sensitive_data(
                    TableColumns.AMOUNT.format.format(coin_data['amount']),
                    privacy_enabled
                ))
                dpg.add_text(mask_sensitive_data(
                    TableColumns.INVESTMENT.format.format(coin_data['investment']),
                    privacy_enabled
                ))
                dpg.add_text(mask_sensitive_data(
                    TableColumns.CURRENT_VALUE.format.format(coin_data['current_value']),
                    privacy_enabled
                ))
                
                profit_color = (0, 255, 0) if coin_data['profit'] >= 0 else (255, 0, 0)
                dpg.add_text(
                    TableColumns.PROFIT.format.format(f"{mask_sensitive_data(f"${coin_data['profit']:,.2f}", privacy_enabled)}\n({f"{coin_data['profit_percentage']:,.2f}%"})"),
                    color=profit_color,
                )

                dpg.add_text(TableColumns.PORTFOLIO_PERCENTAGE.format.format(coin_data['portfolio_percentage']))
                
                with dpg.group():
                    periods = [("24h", "24H"), ("7d", "7D"), ("30d", "30D")]
                    for period_key, period_label in periods:
                        change = coin_data["changes"][period_key]
                        change_color = (0, 255, 0) if change >= 0 else (255, 0, 0)
                        dpg.add_text(
                            f"{period_label}: {change:.2f}%",
                            color=change_color
                        )
                
                with dpg.group():
                    volume_change = coin_data["volume"]["change_24h"]
                    volume_change_color = (0, 255, 0) if volume_change >= 0 else (255, 0, 0)
                    dpg.add_text(
                        f"{volume_change:.2f}%",
                        color=volume_change_color
                    )

                with dpg.group():
                    for i, target in enumerate(coin_data["targets"], start=1):
                        target_price = target['price']
                        is_achieved = coin_data['current_price'] >= target_price
                        dpg.add_text(
                            f"T{i}- {target_price:,.8g}",
                            color=(0, 255, 0) if is_achieved else (255, 255, 255)
                        )
                
                if not privacy_enabled:
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Edit",
                            callback=lambda s, a, u: self.edit_coin(u),
                            user_data=coin_data["db_id"]
                        )
                        dpg.add_button(
                            label="Delete",
                            callback=lambda s, a, u: self.delete_coin(u, coin_data["name"]),
                            user_data=coin_data["db_id"]
                        )

    def edit_coin(self, coin_name):
        EditCoinFrame(self.portfolio, coin_name, self.update_portfolio_view)

    def delete_coin(self, coin_id, coin_name):
        def on_confirm():
            self.portfolio.remove_coin(coin_id)
            self.update_portfolio_view()
            self.portfolio_brief_frame.update_brief()
            dpg.delete_item("confirm_window")
        
        show_confirmation(
            f"Are you sure you want to delete {coin_name}?",
            on_confirm
        )

    def show_error(self, message):
        show_error(message)