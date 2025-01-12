from src.utils import mask_sensitive_data
from src.models import CoinData

from colorama import init, Fore, Style
from tabulate import tabulate
from typing import List

init()

def color_number(value: float, template: str) -> str:
    color = Fore.GREEN if value >= 0 else Fore.RED
    return f"{color}{template}{Style.RESET_ALL}"

def format_portfolio_data(data: List[CoinData], privacy_enabled: bool) -> str:
    sorted_data = sorted(data, key=lambda x: x['profit'], reverse=True)
    
    table_data = []
    for coin in sorted_data:
        profit_text = color_number(
            coin['profit'],
            f"${mask_sensitive_data(f'{coin['profit']:.2f}', privacy_enabled)} ({coin['profit_percentage']:.2f}%)"
        )
        
        changes_24h = color_number(
            coin['changes']['24h'],
            f"{coin['changes']['24h']:.2f}%"
        )
        
        volume_change = color_number(
            coin['volume']['change_24h'],
            f"{coin['volume']['change_24h']:.2f}%"
        )

        targets_text = []
        for i, target in enumerate(coin['targets'], 1):
            price = target['price']
            is_achieved = coin['current_price'] >= price
            color = Fore.GREEN if is_achieved else Style.RESET_ALL
            targets_text.append(f"{color}T{i}- ${price:.8g}{Style.RESET_ALL}")

        table_data.append([
            f"{Fore.CYAN}{coin['db_id']}{Style.RESET_ALL}",
            coin['name'],
            f"${coin['current_price']:.8g}",
            f"${coin['avg_price']:.8g}",
            mask_sensitive_data(f"{coin['amount']:.8g}", privacy_enabled),
            mask_sensitive_data(f"${coin['investment']:.2f}", privacy_enabled),
            mask_sensitive_data(f"${coin['current_value']:.2f}", privacy_enabled),
            profit_text,
            f"{coin['portfolio_percentage']:.2f}%",
            changes_24h,
            volume_change,
            " ".join(targets_text)
        ])
    
    headers = ['ID', 'Name', 'Price', 'Avg Price', 'Amount', 'Investment', 
               'Value', 'Profit/Loss', 'Portfolio %', '24H Change', 
               'Volume Change', 'Targets']
    return tabulate(table_data, headers=headers, tablefmt='grid')

def format_summary(data: List[CoinData], privacy_enabled: bool) -> str:
    total_investment = sum(coin['investment'] for coin in data)
    total_value = sum(coin['current_value'] for coin in data)
    total_profit = total_value - total_investment
    profit_percentage = (total_profit / total_investment * 100) if total_investment > 0 else 0

    profit_text = color_number(
        total_profit,
        f"${mask_sensitive_data(f'{total_profit:,.2f}', privacy_enabled)} ({profit_percentage:.2f}%)"
    )

    summary = [
        f"\n{Fore.CYAN}📊 Portfolio Summary{Style.RESET_ALL}",
        "==================",
        f"Total Investment: ${mask_sensitive_data(f'{total_investment:,.2f}', privacy_enabled)}",
        f"Current Value: ${mask_sensitive_data(f'{total_value:,.2f}', privacy_enabled)}",
        f"Total Profit/Loss: {profit_text}",
        "==================",
    ]
    return "\n".join(summary)

def format_help() -> str:
    commands = [
        ("list", "Show all coins in portfolio"),
        ("add", "Add a new coin"),
        ("edit <id>", "Edit a coin by ID"),
        ("remove <id>", "Remove a coin by ID"),
        ("summary", "Show portfolio summary"),
        ("privacy", "Toggle privacy mode"),
        ("privacy status", "Check privacy mode status"),
        ("help", "Show this help message"),
        ("exit", "Exit the application")
    ]
    
    help_text = [f"\n{Fore.CYAN}Available commands:{Style.RESET_ALL}"]
    for cmd, desc in commands:
        help_text.append(f"  {Fore.GREEN}{cmd:<15}{Style.RESET_ALL} - {desc}")
    return "\n".join(help_text)