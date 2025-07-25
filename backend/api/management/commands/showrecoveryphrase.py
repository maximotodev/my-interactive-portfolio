# backend/api/management/commands/showrecoveryphrase.py

import os
from django.core.management.base import BaseCommand, CommandError
from bitcoinlib.wallets import Wallet, WalletError

class Command(BaseCommand):
    help = 'Displays the recovery information (WIF Private Key) for the portfolio wallet.'

    def handle(self, *args, **options):
        wallet_name = "MyPortfolioWallet"
        self.stdout.write(f"Retrieving recovery information for wallet: '{wallet_name}'")

        try:
            os.environ.setdefault('BITCOINLIB_DATADIR', '.')

            wallet = Wallet(wallet_name)
            
            # --- THIS IS THE FINAL, CORRECT LOGIC BASED ON YOUR DEBUG OUTPUT ---
            # The debug output showed that the wallet object has a 'main_key' attribute.
            master_key = wallet.main_key

            if not master_key:
                raise CommandError("Could not retrieve the master key from the wallet.")
            
            # The debug output showed that the key object has a 'wif' attribute.
            # This is the Wallet Import Format private key.
            if hasattr(master_key, 'wif') and master_key.wif:
                self.stdout.write(self.style.SUCCESS("\n" + "="*50))
                self.stdout.write(self.style.WARNING("  !!! SECURE THIS PRIVATE KEY - DO NOT SHARE IT !!!"))
                self.stdout.write(self.style.SUCCESS("="*50 + "\n"))
                self.stdout.write(f"  Master Private Key (WIF): {master_key.wif}\n")
                self.stdout.write(self.style.SUCCESS("="*50 + "\n"))
                self.stdout.write("Import this WIF key into a wallet like Sparrow or Electrum to access your funds.")
            else:
                raise CommandError("Could not retrieve a WIF private key from the wallet's master key.")


        except WalletError:
            raise CommandError(f"Wallet '{wallet_name}.sqlite' not found. Has a Bitcoin address been requested from the API yet?")
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise CommandError(f"An unexpected error occurred: {e}")