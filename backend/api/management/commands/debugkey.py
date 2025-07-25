# backend/api/management/commands/debugkey.py

import os
from django.core.management.base import BaseCommand, CommandError
from bitcoinlib.wallets import Wallet, WalletError

class Command(BaseCommand):
    help = 'DEBUG COMMAND: Inspects the main_key object to find its attributes.'

    def handle(self, *args, **options):
        wallet_name = "MyPortfolioWallet"
        self.stdout.write(f"--- DEBUGGING WALLET KEY OBJECT: '{wallet_name}' ---")

        try:
            os.environ.setdefault('BITCOINLIB_DATADIR', '.')
            wallet = Wallet(wallet_name)
            
            self.stdout.write(self.style.SUCCESS("\nWallet object has been loaded successfully."))
            
            # Access the main_key attribute which we know exists
            main_key = wallet.main_key

            self.stdout.write("--- Available Attributes and Methods on main_key ---")

            # Use the built-in dir() function to list all attributes and methods
            for attribute in dir(main_key):
                # We will ignore the "private" methods that start with an underscore
                if not attribute.startswith('_'):
                    self.stdout.write(f"- {attribute}")

            self.stdout.write(self.style.SUCCESS("\n--- End of Debugging ---"))
            self.stdout.write("Look for an attribute that seems related to a private key or mnemonic.")


        except WalletError:
            raise CommandError(f"Wallet '{wallet_name}.sqlite' not found.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise CommandError(f"An unexpected error occurred: {e}")