# Separate processes cannot exchange Python objects directly. Serialization
# represents information in a shared format; decoding reconstructs values.
# JSON supports a limited set of values, not arbitrary Python objects.
#
# Convert a product record to field data, then exchange it as JSON text.

import json
from dataclasses import asdict
from m03.catalog import PRODUCTS

product_fields = asdict(PRODUCTS["1"])
message_text = json.dumps(product_fields)
received_fields = json.loads(message_text)

print(type(product_fields).__name__)  # dict
print(type(message_text).__name__)    # str
print(message_text)
print(received_fields["price_paise"]) # 49900

order_request = {"items": [{"product_id": "1", "quantity": 2}]}
print(json.loads(json.dumps(order_request)) == order_request)

# JSON object keys are strings; tuples decode as lists. UUID/date objects
# need explicit representations. A dictionary is not already JSON text.
