from src.cli.formatters import format_portfolio_data, format_summary
from src.utils import validate_coin_input, parse_targets

def handle_command(command: str, portfolio, privacy_manager):
    parts = command.split()
    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    if cmd == "list":
        show_portfolio(portfolio, privacy_manager)
    elif cmd == "add":
        add_coin(portfolio)
    elif cmd == "edit" and args:
        edit_coin(portfolio, int(args[0]))
    elif cmd == "remove" and args:
        remove_coin(portfolio, int(args[0]))
    elif cmd == "summary":
        show_summary(portfolio, privacy_manager)
    else:
        print("Unknown command. Type 'help' for available commands.")

def show_portfolio(portfolio, privacy_manager):
    data = portfolio.get_portfolio_data()
    if not data:
        print("Portfolio is empty!")
        return
    print(format_portfolio_data(data, privacy_manager.is_privacy_enabled()))

def show_summary(portfolio, privacy_manager):
    data = portfolio.get_portfolio_data()
    if not data:
        print("Portfolio is empty!")
        return
    print(format_summary(data, privacy_manager.is_privacy_enabled()))

def add_coin(portfolio):
    print("\nAdd new coin:")
    try:
        name = input("Coin name: ").strip()
        coin_id = input("CoinMarketCap ID: ").strip()
        avg_price = float(input("Average buy price ($): "))
        amount = float(input("Amount: "))
        targets = input("Target prices (comma-separated, optional): ").strip()

        validate_coin_input(name, coin_id, avg_price, amount)
        targets_list = parse_targets(targets) if targets else []

        portfolio.add_coin(name, coin_id, avg_price, amount, targets_list)
        print(f"\n✅ Successfully added {name} to portfolio!")
    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")

def edit_coin(portfolio, coin_id):
    try:
        coin = portfolio.get_coin(coin_id)
        print(f"\nEditing {coin['name']}:")
        
        name = input(f"New name [Leave blank to keep {coin['name']}]: ").strip() or coin['name']
        cmc_coin_id = input(f"New CoinMarketCap ID [Leave blank to keep {coin['id']}]: ").strip() or coin['id']
        avg_price = float(input(f"New average price [Leave blank to keep {coin['avg_price']}]: ") or coin['avg_price'])
        amount = float(input(f"New amount [Leave blank to keep {coin['amount']}]: ") or coin['amount'])
        current_targets = ",".join(map(str, coin['targets']))
        targets = input(f"New target prices [Leave blank to keep {current_targets}]: ").strip() or current_targets

        validate_coin_input(name, coin_id, avg_price, amount)
        targets_list = parse_targets(targets) if targets else []

        portfolio.update_coin(coin_id, name, cmc_coin_id, avg_price, amount, targets_list)
        print(f"\n✅ Successfully updated {name}!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def remove_coin(portfolio, coin_id):
    try:
        coin = portfolio.get_coin(coin_id)
        confirm = input(f"\nAre you sure you want to remove {coin['name']}? (y/N): ").lower()
        if confirm == 'y':
            portfolio.remove_coin(coin_id)
            print(f"\n✅ Successfully removed {coin['name']}!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}") 