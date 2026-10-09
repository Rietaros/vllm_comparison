Stock check for item $item at the Bandung shop.
Opening stock is zero. Every receipt below was accepted and is a separate delivery.
$receipts
Already reserved: $reserved units. A new customer requests $requested units.
Available stock = accepted receipts minus existing reservations.
Example JSON format only (illustrative values, not the answer):
$output_example
Calculate your actual values from the data. Return integer results, not arithmetic expressions.
Return JSON only with exactly these keys: "item" (the item name only), "available_units" (integer), "fulfillable" (boolean: available stock >= the new request).
