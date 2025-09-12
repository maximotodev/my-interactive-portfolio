# backend/api/management/commands/listen_for_listings.py
import json
import time
from django.core.management.base import BaseCommand
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
# --- UPDATED IMPORTS ---
from api.nostr_utils import save_stall_from_event, save_product_from_event

# NIP-15 Event Kinds
STALL_KIND = 30017
PRODUCT_KIND = 30018

class Command(BaseCommand):
    help = 'Listens to Nostr relays for NIP-15 marketplace events and saves them.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Starting NIP-15 Marketplace Listener ---"))
        
        relay_manager = RelayManager(timeout=6)
        relay_manager.add_relay("wss://relay.damus.io")
        relay_manager.add_relay("wss://relay.primal.net")
        relay_manager.add_relay("wss://nos.lol")
        relay_manager.add_relay("wss://relay.nostr.band")

        filters = FiltersList([Filters(kinds=[STALL_KIND, PRODUCT_KIND])])
        subscription_id = "marketplace_nip15_sub"
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        
        try:
            while True:
                self.stdout.write(f"({time.strftime('%H:%M:%S')}) Listening for NIP-15 events...")
                relay_manager.run_sync()
                
                while relay_manager.message_pool.has_events():
                    event_msg = relay_manager.message_pool.get_event()
                    event = event_msg.event
                    
                    if event.kind == STALL_KIND:
                        stall = save_stall_from_event(event)
                        if stall:
                            self.stdout.write(self.style.SUCCESS(f"  + Saved/Updated Stall: '{stall.name}'"))
                    
                    elif event.kind == PRODUCT_KIND:
                        product = save_product_from_event(event)
                        if product:
                            self.stdout.write(self.style.SUCCESS(f"  + Saved/Updated Product: '{product.name}'"))

                time.sleep(30)

        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("\n--- Listener stopped manually. ---"))
        finally:
            self.stdout.write("Closing relay connections...")
            relay_manager.close_all_relay_connections()