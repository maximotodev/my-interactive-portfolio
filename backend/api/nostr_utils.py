# backend/api/nostr_utils.py
import json
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError
from .models import Stall, Product

# --- NIP-15 Schemas for Validation (No changes here) ---
class ShippingZoneSchema(BaseModel):
    id: str
    name: Optional[str] = None
    cost: float
    regions: List[str]

class Nip15StallSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    currency: str
    shipping: List[ShippingZoneSchema] = []

class ProductShippingCostSchema(BaseModel):
    id: str
    cost: float

class Nip15ProductSchema(BaseModel):
    id: str
    stall_id: str
    name: str
    description: Optional[str] = None
    images: Optional[List[str]] = []
    currency: str
    price: float
    quantity: Optional[int] = None
    specs: Optional[List[Tuple[str, str]]] = []
    shipping: Optional[List[ProductShippingCostSchema]] = []

def get_event_tag_value(event, tag_key):
    for tag in event.tags:
        if tag[0] == tag_key:
            return tag[1]
    return None

def save_stall_from_event(event):
    """Validates a Nostr event for a Stall and saves it to the database."""
    try:
        data = json.loads(event.content)

        # --- THIS IS THE FIX ---
        # Some clients send a list instead of a dict. We must ignore these.
        if not isinstance(data, dict):
            return None

        stall_data = Nip15StallSchema(**data)
        stall_id = get_event_tag_value(event, 'd')
        if not stall_id or stall_id != stall_data.id: return None

        stall, created = Stall.objects.update_or_create(
            id=stall_data.id,
            defaults={
                'merchant_pubkey': event.pubkey,
                'name': stall_data.name,
                'description': stall_data.description,
                'currency': stall_data.currency,
                'shipping_zones': [zone.dict() for zone in stall_data.shipping],
                'created_at': datetime.fromtimestamp(event.created_at, tz=timezone.utc),
            }
        )
        return stall
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Failed to validate/save stall event {event.id}: {e}")
        return None

def save_product_from_event(event):
    """Validates a Nostr event for a Product and saves it to the database."""
    try:
        data = json.loads(event.content)
        
        # Also add the protection here for malformed product events
        if not isinstance(data, dict):
            return None
            
        stall_id = data.get('stall_id')
        if not stall_id: return None
        
        stall = Stall.objects.get(id=stall_id)
        product_data = Nip15ProductSchema(**data)
        product_id = get_event_tag_value(event, 'd')
        if not product_id or product_id != product_data.id: return None
        
        category_tags = [tag[1] for tag in event.tags if tag[0] == 't']

        product, created = Product.objects.update_or_create(
            id=product_data.id,
            defaults={
                'stall': stall,
                'name': product_data.name,
                'description': product_data.description,
                'images': product_data.images,
                'currency': product_data.currency,
                'price': product_data.price,
                'quantity': product_data.quantity,
                'specs': product_data.specs,
                'shipping': [s.dict() for s in product_data.shipping],
                'tags': category_tags,
                'event_id': event.id,
                'merchant_pubkey': event.pubkey,
                'created_at': datetime.fromtimestamp(event.created_at, tz=timezone.utc),
            }
        )
        return product
    except Stall.DoesNotExist:
        print(f"Stall with ID '{stall_id}' not found for product event {event.id}.")
        return None
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Failed to validate/save product event {event.id}: {e}")
        return None