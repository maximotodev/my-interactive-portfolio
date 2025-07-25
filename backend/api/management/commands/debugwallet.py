# backend/api/management/commands/debugwallet.py

import os
from django.core.management.base import BaseCommand, CommandError
from bitcoinlib.wallets import Wallet, WalletError

class Command(BaseCommand):
    help = 'DEBUG COMMAND: Inspects the wallet object to find its attributes.'

    def handle(self, *args, **options):
        wallet_name = "MyPortfolioWallet"
        self.stdout.write(f"--- DEBUGGING WALLET OBJECT: '{wallet_name}' ---")

        try:
            os.environ.setdefault('BITCOINLIB_DATADIR', '.')
            wallet = Wallet(wallet_name)
            
            self.stdout.write(self.style.SUCCESS("\nWallet object has been loaded successfully."))
            self.stdout.write("--- Available Attributes and Methods ---")

            # Use the built-in dir() function to list all attributes and methods
            for attribute in dir(wallet):
                # We will ignore the "private" methods that start with an underscore
                if not attribute.startswith('_'):
                    self.stdout.write(f"- {attribute}")

            self.stdout.write(self.style.SUCCESS("\n--- End of Debugging ---"))
            self.stdout.write("Look for an attribute that seems related to keys, like 'key', 'keys', 'masterkey', etc.")


        except WalletError:
            raise CommandError(f"Wallet '{wallet_name}.sqlite' not found.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise CommandError(f"An unexpected error occurred: {e}")