from src.utils import logger, PrivacyManager
from src.cli.commands import handle_command
from src.cli.formatters import format_help
from src.models import Portfolio

from colorama import Fore, Style
from getpass import getpass

class CliApp:
    def __init__(self):
        self.portfolio = Portfolio()
        self.privacy_manager = PrivacyManager()
        self.running = True
        
    def display_help(self):
        print(format_help())

    def handle_privacy_command(self, args):
        if not args:
            if self.privacy_manager.is_privacy_enabled():
                password = getpass("Enter password to disable privacy mode: ")
                if self.privacy_manager.toggle_privacy(password):
                    print(f"\n{Fore.GREEN}✓ Privacy mode disabled{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}✗ Incorrect password{Style.RESET_ALL}")
            else:
                self.privacy_manager.toggle_privacy()
                print(f"\n{Fore.GREEN}✓ Privacy mode enabled{Style.RESET_ALL}")
        elif args[0] == "status":
            status = "enabled" if self.privacy_manager.is_privacy_enabled() else "disabled"
            print(f"\nPrivacy mode is currently {status}")

    def run(self):
        print("\n🚀 Welcome to Crypto Portfolio Tracker CLI!")
        self.display_help()
        
        while self.running:
            try:
                command = input("\n> ").strip().lower()
                parts = command.split()
                cmd = parts[0] if parts else ""
                args = parts[1:] if len(parts) > 1 else []

                if cmd == "exit":
                    self.running = False
                    print("Goodbye! 👋")
                elif cmd == "help":
                    self.display_help()
                elif cmd == "privacy":
                    self.handle_privacy_command(args)
                else:
                    handle_command(command, self.portfolio, self.privacy_manager)
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}") 