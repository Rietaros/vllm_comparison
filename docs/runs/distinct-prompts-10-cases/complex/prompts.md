# Complete benchmark prompt cases

Suite: editable-distinct-cases-v5

System message: Use only the supplied data. Apply every stated rule and return the requested JSON.

## Short / short-01 / trial 1

Short case 01: monitor decision.

Input tokens including chat template: 251. Budget: 256.

Reference answer: `{"item": "MONITOR", "available_units": 124, "fulfillable": true}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for MONITOR at shop S01.
Opening usable stock: 23 units.
All receipts below are accepted, separate deliveries:
Receipt R0101: 10 units.
Receipt R0102: 15 units.
Receipt R0103: 20 units.
Receipt R0104: 6 units.
Receipt R0105: 11 units.
Receipt R0106: 16 units.
Receipt R0107: 21 units.
Receipt R0108: 7 units.
Existing reservations: 5 units. New customer request: 37 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-02 / trial 2

Short case 02: keyboard decision.

Input tokens including chat template: 250. Budget: 256.

Reference answer: `{"item": "KEYBOARD", "available_units": 113, "fulfillable": false}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for KEYBOARD at shop S02.
Opening usable stock: 34 units.
All receipts below are accepted, separate deliveries:
Receipt R0201: 17 units.
Receipt R0202: 3 units.
Receipt R0203: 8 units.
Receipt R0204: 13 units.
Receipt R0205: 18 units.
Receipt R0206: 4 units.
Receipt R0207: 9 units.
Receipt R0208: 14 units.
Existing reservations: 7 units. New customer request: 200 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-03 / trial 3

Short case 03: router decision.

Input tokens including chat template: 251. Budget: 256.

Reference answer: `{"item": "ROUTER", "available_units": 140, "fulfillable": true}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for ROUTER at shop S03.
Opening usable stock: 45 units.
All receipts below are accepted, separate deliveries:
Receipt R0301: 5 units.
Receipt R0302: 10 units.
Receipt R0303: 15 units.
Receipt R0304: 20 units.
Receipt R0305: 6 units.
Receipt R0306: 11 units.
Receipt R0307: 16 units.
Receipt R0308: 21 units.
Existing reservations: 9 units. New customer request: 47 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-04 / trial 4

Short case 04: printer decision.

Input tokens including chat template: 251. Budget: 256.

Reference answer: `{"item": "PRINTER", "available_units": 129, "fulfillable": false}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for PRINTER at shop S04.
Opening usable stock: 56 units.
All receipts below are accepted, separate deliveries:
Receipt R0401: 12 units.
Receipt R0402: 17 units.
Receipt R0403: 3 units.
Receipt R0404: 8 units.
Receipt R0405: 13 units.
Receipt R0406: 18 units.
Receipt R0407: 4 units.
Receipt R0408: 9 units.
Existing reservations: 11 units. New customer request: 230 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-05 / trial 5

Short case 05: tablet decision.

Input tokens including chat template: 252. Budget: 256.

Reference answer: `{"item": "TABLET", "available_units": 156, "fulfillable": true}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for TABLET at shop S05.
Opening usable stock: 67 units.
All receipts below are accepted, separate deliveries:
Receipt R0501: 19 units.
Receipt R0502: 5 units.
Receipt R0503: 10 units.
Receipt R0504: 15 units.
Receipt R0505: 20 units.
Receipt R0506: 6 units.
Receipt R0507: 11 units.
Receipt R0508: 16 units.
Existing reservations: 13 units. New customer request: 57 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-06 / trial 6

Short case 06: scanner decision.

Input tokens including chat template: 251. Budget: 256.

Reference answer: `{"item": "SCANNER", "available_units": 145, "fulfillable": false}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for SCANNER at shop S06.
Opening usable stock: 78 units.
All receipts below are accepted, separate deliveries:
Receipt R0601: 7 units.
Receipt R0602: 12 units.
Receipt R0603: 17 units.
Receipt R0604: 3 units.
Receipt R0605: 8 units.
Receipt R0606: 13 units.
Receipt R0607: 18 units.
Receipt R0608: 4 units.
Existing reservations: 15 units. New customer request: 260 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-07 / trial 7

Short case 07: webcam decision.

Input tokens including chat template: 253. Budget: 256.

Reference answer: `{"item": "WEBCAM", "available_units": 172, "fulfillable": true}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for WEBCAM at shop S07.
Opening usable stock: 89 units.
All receipts below are accepted, separate deliveries:
Receipt R0701: 14 units.
Receipt R0702: 19 units.
Receipt R0703: 5 units.
Receipt R0704: 10 units.
Receipt R0705: 15 units.
Receipt R0706: 20 units.
Receipt R0707: 6 units.
Receipt R0708: 11 units.
Existing reservations: 17 units. New customer request: 67 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-08 / trial 8

Short case 08: headset decision.

Input tokens including chat template: 253. Budget: 256.

Reference answer: `{"item": "HEADSET", "available_units": 180, "fulfillable": false}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for HEADSET at shop S08.
Opening usable stock: 100 units.
All receipts below are accepted, separate deliveries:
Receipt R0801: 21 units.
Receipt R0802: 7 units.
Receipt R0803: 12 units.
Receipt R0804: 17 units.
Receipt R0805: 3 units.
Receipt R0806: 8 units.
Receipt R0807: 13 units.
Receipt R0808: 18 units.
Existing reservations: 19 units. New customer request: 290 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-09 / trial 9

Short case 09: speaker decision.

Input tokens including chat template: 252. Budget: 256.

Reference answer: `{"item": "SPEAKER", "available_units": 188, "fulfillable": true}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for SPEAKER at shop S09.
Opening usable stock: 111 units.
All receipts below are accepted, separate deliveries:
Receipt R0901: 9 units.
Receipt R0902: 14 units.
Receipt R0903: 19 units.
Receipt R0904: 5 units.
Receipt R0905: 10 units.
Receipt R0906: 15 units.
Receipt R0907: 20 units.
Receipt R0908: 6 units.
Existing reservations: 21 units. New customer request: 77 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Short / short-10 / trial 10

Short case 10: projector decision.

Input tokens including chat template: 253. Budget: 256.

Reference answer: `{"item": "PROJECTOR", "available_units": 196, "fulfillable": false}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Inventory decision for PROJECTOR at shop S10.
Opening usable stock: 122 units.
All receipts below are accepted, separate deliveries:
Receipt R1001: 16 units.
Receipt R1002: 21 units.
Receipt R1003: 7 units.
Receipt R1004: 12 units.
Receipt R1005: 17 units.
Receipt R1006: 3 units.
Receipt R1007: 8 units.
Receipt R1008: 13 units.
Existing reservations: 23 units. New customer request: 320 units.
Available stock = opening stock + all accepted receipts - existing reservations.
Fulfillable means available stock is at least the new customer request.
Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.
Calculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).
```

## Medium / medium-01 / trial 1

Medium case 01: monitor decision.

Input tokens including chat template: 1015. Budget: 1024.

Reference answer: `{"vendor": "V01-07", "landed_cost": 832, "eligible_vendors": 8, "delivery_days": 1}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M01: buy 99 monitor units in one order.
Delivery deadline: 4 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V01-01: unit price 11; shipping 41; fixed discount 5; delivery 1 days; capacity 124 units; certified yes.
V01-02: unit price 18; shipping 58; fixed discount 18; delivery 2 days; capacity 124 units; certified yes.
V01-03: unit price 10; shipping 75; fixed discount 31; delivery 4 days; capacity 125 units; certified yes.
V01-04: unit price 17; shipping 92; fixed discount 9; delivery 5 days; capacity 148 units; certified no.
V01-05: unit price 9; shipping 109; fixed discount 22; delivery 6 days; capacity 171 units; certified yes.
V01-06: unit price 16; shipping 36; fixed discount 0; delivery 7 days; capacity 194 units; certified yes.
V01-07: unit price 8; shipping 53; fixed discount 13; delivery 1 days; capacity 217 units; certified yes.
V01-08: unit price 15; shipping 70; fixed discount 26; delivery 2 days; capacity 60 units; certified no.
V01-09: unit price 22; shipping 87; fixed discount 4; delivery 3 days; capacity 83 units; certified yes.
V01-10: unit price 14; shipping 104; fixed discount 17; delivery 4 days; capacity 106 units; certified yes.
V01-11: unit price 21; shipping 31; fixed discount 30; delivery 5 days; capacity 129 units; certified yes.
V01-12: unit price 13; shipping 48; fixed discount 8; delivery 6 days; capacity 152 units; certified no.
V01-13: unit price 20; shipping 65; fixed discount 21; delivery 7 days; capacity 175 units; certified yes.
V01-14: unit price 12; shipping 82; fixed discount 34; delivery 1 days; capacity 198 units; certified yes.
V01-15: unit price 19; shipping 99; fixed discount 12; delivery 2 days; capacity 221 units; certified yes.
V01-16: unit price 11; shipping 116; fixed discount 25; delivery 3 days; capacity 64 units; certified no.
V01-17: unit price 18; shipping 43; fixed discount 3; delivery 4 days; capacity 87 units; certified yes.
V01-18: unit price 10; shipping 60; fixed discount 16; delivery 5 days; capacity 110 units; certified yes.
V01-19: unit price 17; shipping 77; fixed discount 29; delivery 6 days; capacity 133 units; certified yes.
V01-20: unit price 9; shipping 94; fixed discount 7; delivery 7 days; capacity 156 units; certified no.
V01-21: unit price 16; shipping 111; fixed discount 20; delivery 1 days; capacity 179 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-02 / trial 2

Medium case 02: keyboard decision.

Input tokens including chat template: 1019. Budget: 1024.

Reference answer: `{"vendor": "V02-13", "landed_cost": 914, "eligible_vendors": 8, "delivery_days": 1}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M02: buy 108 keyboard units in one order.
Delivery deadline: 5 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V02-01: unit price 14; shipping 52; fixed discount 10; delivery 1 days; capacity 133 units; certified yes.
V02-02: unit price 21; shipping 69; fixed discount 23; delivery 2 days; capacity 133 units; certified yes.
V02-03: unit price 13; shipping 86; fixed discount 1; delivery 5 days; capacity 144 units; certified no.
V02-04: unit price 20; shipping 103; fixed discount 14; delivery 6 days; capacity 167 units; certified yes.
V02-05: unit price 12; shipping 30; fixed discount 27; delivery 7 days; capacity 190 units; certified yes.
V02-06: unit price 19; shipping 47; fixed discount 5; delivery 1 days; capacity 213 units; certified yes.
V02-07: unit price 11; shipping 64; fixed discount 18; delivery 2 days; capacity 236 units; certified no.
V02-08: unit price 18; shipping 81; fixed discount 31; delivery 3 days; capacity 79 units; certified yes.
V02-09: unit price 10; shipping 98; fixed discount 9; delivery 4 days; capacity 102 units; certified yes.
V02-10: unit price 17; shipping 115; fixed discount 22; delivery 5 days; capacity 125 units; certified yes.
V02-11: unit price 9; shipping 42; fixed discount 0; delivery 6 days; capacity 148 units; certified no.
V02-12: unit price 16; shipping 59; fixed discount 13; delivery 7 days; capacity 171 units; certified yes.
V02-13: unit price 8; shipping 76; fixed discount 26; delivery 1 days; capacity 194 units; certified yes.
V02-14: unit price 15; shipping 93; fixed discount 4; delivery 2 days; capacity 217 units; certified yes.
V02-15: unit price 22; shipping 110; fixed discount 17; delivery 3 days; capacity 60 units; certified no.
V02-16: unit price 14; shipping 37; fixed discount 30; delivery 4 days; capacity 83 units; certified yes.
V02-17: unit price 21; shipping 54; fixed discount 8; delivery 5 days; capacity 106 units; certified yes.
V02-18: unit price 13; shipping 71; fixed discount 21; delivery 6 days; capacity 129 units; certified yes.
V02-19: unit price 20; shipping 88; fixed discount 34; delivery 7 days; capacity 152 units; certified no.
V02-20: unit price 12; shipping 105; fixed discount 12; delivery 1 days; capacity 175 units; certified yes.
V02-21: unit price 19; shipping 32; fixed discount 25; delivery 2 days; capacity 198 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-03 / trial 3

Medium case 03: router decision.

Input tokens including chat template: 1017. Budget: 1024.

Reference answer: `{"vendor": "V03-19", "landed_cost": 1031, "eligible_vendors": 8, "delivery_days": 1}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M03: buy 117 router units in one order.
Delivery deadline: 3 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V03-01: unit price 17; shipping 63; fixed discount 15; delivery 1 days; capacity 142 units; certified yes.
V03-02: unit price 9; shipping 80; fixed discount 28; delivery 2 days; capacity 142 units; certified yes.
V03-03: unit price 16; shipping 97; fixed discount 6; delivery 6 days; capacity 163 units; certified yes.
V03-04: unit price 8; shipping 114; fixed discount 19; delivery 7 days; capacity 186 units; certified yes.
V03-05: unit price 15; shipping 41; fixed discount 32; delivery 1 days; capacity 209 units; certified yes.
V03-06: unit price 22; shipping 58; fixed discount 10; delivery 2 days; capacity 232 units; certified no.
V03-07: unit price 14; shipping 75; fixed discount 23; delivery 3 days; capacity 75 units; certified yes.
V03-08: unit price 21; shipping 92; fixed discount 1; delivery 4 days; capacity 98 units; certified yes.
V03-09: unit price 13; shipping 109; fixed discount 14; delivery 5 days; capacity 121 units; certified yes.
V03-10: unit price 20; shipping 36; fixed discount 27; delivery 6 days; capacity 144 units; certified no.
V03-11: unit price 12; shipping 53; fixed discount 5; delivery 7 days; capacity 167 units; certified yes.
V03-12: unit price 19; shipping 70; fixed discount 18; delivery 1 days; capacity 190 units; certified yes.
V03-13: unit price 11; shipping 87; fixed discount 31; delivery 2 days; capacity 213 units; certified yes.
V03-14: unit price 18; shipping 104; fixed discount 9; delivery 3 days; capacity 236 units; certified no.
V03-15: unit price 10; shipping 31; fixed discount 22; delivery 4 days; capacity 79 units; certified yes.
V03-16: unit price 17; shipping 48; fixed discount 0; delivery 5 days; capacity 102 units; certified yes.
V03-17: unit price 9; shipping 65; fixed discount 13; delivery 6 days; capacity 125 units; certified yes.
V03-18: unit price 16; shipping 82; fixed discount 26; delivery 7 days; capacity 148 units; certified no.
V03-19: unit price 8; shipping 99; fixed discount 4; delivery 1 days; capacity 171 units; certified yes.
V03-20: unit price 15; shipping 116; fixed discount 17; delivery 2 days; capacity 194 units; certified yes.
V03-21: unit price 22; shipping 43; fixed discount 30; delivery 3 days; capacity 217 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-04 / trial 4

Medium case 04: printer decision.

Input tokens including chat template: 1018. Budget: 1024.

Reference answer: `{"vendor": "V04-04", "landed_cost": 1397, "eligible_vendors": 8, "delivery_days": 1}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M04: buy 126 printer units in one order.
Delivery deadline: 4 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V04-01: unit price 20; shipping 74; fixed discount 20; delivery 1 days; capacity 151 units; certified yes.
V04-02: unit price 12; shipping 91; fixed discount 33; delivery 2 days; capacity 151 units; certified yes.
V04-03: unit price 19; shipping 108; fixed discount 11; delivery 7 days; capacity 182 units; certified yes.
V04-04: unit price 11; shipping 35; fixed discount 24; delivery 1 days; capacity 205 units; certified yes.
V04-05: unit price 18; shipping 52; fixed discount 2; delivery 2 days; capacity 228 units; certified no.
V04-06: unit price 10; shipping 69; fixed discount 15; delivery 3 days; capacity 71 units; certified yes.
V04-07: unit price 17; shipping 86; fixed discount 28; delivery 4 days; capacity 94 units; certified yes.
V04-08: unit price 9; shipping 103; fixed discount 6; delivery 5 days; capacity 117 units; certified yes.
V04-09: unit price 16; shipping 30; fixed discount 19; delivery 6 days; capacity 140 units; certified no.
V04-10: unit price 8; shipping 47; fixed discount 32; delivery 7 days; capacity 163 units; certified yes.
V04-11: unit price 15; shipping 64; fixed discount 10; delivery 1 days; capacity 186 units; certified yes.
V04-12: unit price 22; shipping 81; fixed discount 23; delivery 2 days; capacity 209 units; certified yes.
V04-13: unit price 14; shipping 98; fixed discount 1; delivery 3 days; capacity 232 units; certified no.
V04-14: unit price 21; shipping 115; fixed discount 14; delivery 4 days; capacity 75 units; certified yes.
V04-15: unit price 13; shipping 42; fixed discount 27; delivery 5 days; capacity 98 units; certified yes.
V04-16: unit price 20; shipping 59; fixed discount 5; delivery 6 days; capacity 121 units; certified yes.
V04-17: unit price 12; shipping 76; fixed discount 18; delivery 7 days; capacity 144 units; certified no.
V04-18: unit price 19; shipping 93; fixed discount 31; delivery 1 days; capacity 167 units; certified yes.
V04-19: unit price 11; shipping 110; fixed discount 9; delivery 2 days; capacity 190 units; certified yes.
V04-20: unit price 18; shipping 37; fixed discount 22; delivery 3 days; capacity 213 units; certified yes.
V04-21: unit price 10; shipping 54; fixed discount 0; delivery 4 days; capacity 236 units; certified no.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-05 / trial 5

Medium case 05: tablet decision.

Input tokens including chat template: 1017. Budget: 1024.

Reference answer: `{"vendor": "V05-01", "landed_cost": 1140, "eligible_vendors": 8, "delivery_days": 1}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M05: buy 135 tablet units in one order.
Delivery deadline: 5 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V05-01: unit price 8; shipping 85; fixed discount 25; delivery 1 days; capacity 160 units; certified yes.
V05-02: unit price 15; shipping 102; fixed discount 3; delivery 2 days; capacity 160 units; certified yes.
V05-03: unit price 22; shipping 119; fixed discount 16; delivery 1 days; capacity 201 units; certified yes.
V05-04: unit price 14; shipping 46; fixed discount 29; delivery 2 days; capacity 224 units; certified no.
V05-05: unit price 21; shipping 63; fixed discount 7; delivery 3 days; capacity 67 units; certified yes.
V05-06: unit price 13; shipping 80; fixed discount 20; delivery 4 days; capacity 90 units; certified yes.
V05-07: unit price 20; shipping 97; fixed discount 33; delivery 5 days; capacity 113 units; certified yes.
V05-08: unit price 12; shipping 114; fixed discount 11; delivery 6 days; capacity 136 units; certified no.
V05-09: unit price 19; shipping 41; fixed discount 24; delivery 7 days; capacity 159 units; certified yes.
V05-10: unit price 11; shipping 58; fixed discount 2; delivery 1 days; capacity 182 units; certified yes.
V05-11: unit price 18; shipping 75; fixed discount 15; delivery 2 days; capacity 205 units; certified yes.
V05-12: unit price 10; shipping 92; fixed discount 28; delivery 3 days; capacity 228 units; certified no.
V05-13: unit price 17; shipping 109; fixed discount 6; delivery 4 days; capacity 71 units; certified yes.
V05-14: unit price 9; shipping 36; fixed discount 19; delivery 5 days; capacity 94 units; certified yes.
V05-15: unit price 16; shipping 53; fixed discount 32; delivery 6 days; capacity 117 units; certified yes.
V05-16: unit price 8; shipping 70; fixed discount 10; delivery 7 days; capacity 140 units; certified no.
V05-17: unit price 15; shipping 87; fixed discount 23; delivery 1 days; capacity 163 units; certified yes.
V05-18: unit price 22; shipping 104; fixed discount 1; delivery 2 days; capacity 186 units; certified yes.
V05-19: unit price 14; shipping 31; fixed discount 14; delivery 3 days; capacity 209 units; certified yes.
V05-20: unit price 21; shipping 48; fixed discount 27; delivery 4 days; capacity 232 units; certified no.
V05-21: unit price 13; shipping 65; fixed discount 5; delivery 5 days; capacity 75 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-06 / trial 6

Medium case 06: scanner decision.

Input tokens including chat template: 1016. Budget: 1024.

Reference answer: `{"vendor": "V06-18", "landed_cost": 1549, "eligible_vendors": 7, "delivery_days": 3}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M06: buy 144 scanner units in one order.
Delivery deadline: 3 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V06-01: unit price 11; shipping 96; fixed discount 30; delivery 1 days; capacity 169 units; certified yes.
V06-02: unit price 18; shipping 113; fixed discount 8; delivery 2 days; capacity 169 units; certified yes.
V06-03: unit price 10; shipping 40; fixed discount 21; delivery 2 days; capacity 220 units; certified no.
V06-04: unit price 17; shipping 57; fixed discount 34; delivery 3 days; capacity 63 units; certified yes.
V06-05: unit price 9; shipping 74; fixed discount 12; delivery 4 days; capacity 86 units; certified yes.
V06-06: unit price 16; shipping 91; fixed discount 25; delivery 5 days; capacity 109 units; certified yes.
V06-07: unit price 8; shipping 108; fixed discount 3; delivery 6 days; capacity 132 units; certified no.
V06-08: unit price 15; shipping 35; fixed discount 16; delivery 7 days; capacity 155 units; certified yes.
V06-09: unit price 22; shipping 52; fixed discount 29; delivery 1 days; capacity 178 units; certified yes.
V06-10: unit price 14; shipping 69; fixed discount 7; delivery 2 days; capacity 201 units; certified yes.
V06-11: unit price 21; shipping 86; fixed discount 20; delivery 3 days; capacity 224 units; certified no.
V06-12: unit price 13; shipping 103; fixed discount 33; delivery 4 days; capacity 67 units; certified yes.
V06-13: unit price 20; shipping 30; fixed discount 11; delivery 5 days; capacity 90 units; certified yes.
V06-14: unit price 12; shipping 47; fixed discount 24; delivery 6 days; capacity 113 units; certified yes.
V06-15: unit price 19; shipping 64; fixed discount 2; delivery 7 days; capacity 136 units; certified no.
V06-16: unit price 11; shipping 81; fixed discount 15; delivery 1 days; capacity 159 units; certified yes.
V06-17: unit price 18; shipping 98; fixed discount 28; delivery 2 days; capacity 182 units; certified yes.
V06-18: unit price 10; shipping 115; fixed discount 6; delivery 3 days; capacity 205 units; certified yes.
V06-19: unit price 17; shipping 42; fixed discount 19; delivery 4 days; capacity 228 units; certified no.
V06-20: unit price 9; shipping 59; fixed discount 32; delivery 5 days; capacity 71 units; certified yes.
V06-21: unit price 16; shipping 76; fixed discount 10; delivery 6 days; capacity 94 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-07 / trial 7

Medium case 07: webcam decision.

Input tokens including chat template: 1018. Budget: 1024.

Reference answer: `{"vendor": "V07-09", "landed_cost": 1559, "eligible_vendors": 8, "delivery_days": 2}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M07: buy 153 webcam units in one order.
Delivery deadline: 4 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V07-01: unit price 14; shipping 107; fixed discount 0; delivery 1 days; capacity 178 units; certified yes.
V07-02: unit price 21; shipping 34; fixed discount 13; delivery 2 days; capacity 178 units; certified yes.
V07-03: unit price 13; shipping 51; fixed discount 26; delivery 3 days; capacity 239 units; certified yes.
V07-04: unit price 20; shipping 68; fixed discount 4; delivery 4 days; capacity 82 units; certified yes.
V07-05: unit price 12; shipping 85; fixed discount 17; delivery 5 days; capacity 105 units; certified yes.
V07-06: unit price 19; shipping 102; fixed discount 30; delivery 6 days; capacity 128 units; certified no.
V07-07: unit price 11; shipping 119; fixed discount 8; delivery 7 days; capacity 151 units; certified yes.
V07-08: unit price 18; shipping 46; fixed discount 21; delivery 1 days; capacity 174 units; certified yes.
V07-09: unit price 10; shipping 63; fixed discount 34; delivery 2 days; capacity 197 units; certified yes.
V07-10: unit price 17; shipping 80; fixed discount 12; delivery 3 days; capacity 220 units; certified no.
V07-11: unit price 9; shipping 97; fixed discount 25; delivery 4 days; capacity 63 units; certified yes.
V07-12: unit price 16; shipping 114; fixed discount 3; delivery 5 days; capacity 86 units; certified yes.
V07-13: unit price 8; shipping 41; fixed discount 16; delivery 6 days; capacity 109 units; certified yes.
V07-14: unit price 15; shipping 58; fixed discount 29; delivery 7 days; capacity 132 units; certified no.
V07-15: unit price 22; shipping 75; fixed discount 7; delivery 1 days; capacity 155 units; certified yes.
V07-16: unit price 14; shipping 92; fixed discount 20; delivery 2 days; capacity 178 units; certified yes.
V07-17: unit price 21; shipping 109; fixed discount 33; delivery 3 days; capacity 201 units; certified yes.
V07-18: unit price 13; shipping 36; fixed discount 11; delivery 4 days; capacity 224 units; certified no.
V07-19: unit price 20; shipping 53; fixed discount 24; delivery 5 days; capacity 67 units; certified yes.
V07-20: unit price 12; shipping 70; fixed discount 2; delivery 6 days; capacity 90 units; certified yes.
V07-21: unit price 19; shipping 87; fixed discount 15; delivery 7 days; capacity 113 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-08 / trial 8

Medium case 08: headset decision.

Input tokens including chat template: 1015. Budget: 1024.

Reference answer: `{"vendor": "V08-02", "landed_cost": 1485, "eligible_vendors": 7, "delivery_days": 2}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M08: buy 162 headset units in one order.
Delivery deadline: 5 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V08-01: unit price 17; shipping 118; fixed discount 5; delivery 1 days; capacity 187 units; certified yes.
V08-02: unit price 9; shipping 45; fixed discount 18; delivery 2 days; capacity 187 units; certified yes.
V08-03: unit price 16; shipping 62; fixed discount 31; delivery 4 days; capacity 78 units; certified yes.
V08-04: unit price 8; shipping 79; fixed discount 9; delivery 5 days; capacity 101 units; certified yes.
V08-05: unit price 15; shipping 96; fixed discount 22; delivery 6 days; capacity 124 units; certified no.
V08-06: unit price 22; shipping 113; fixed discount 0; delivery 7 days; capacity 147 units; certified yes.
V08-07: unit price 14; shipping 40; fixed discount 13; delivery 1 days; capacity 170 units; certified yes.
V08-08: unit price 21; shipping 57; fixed discount 26; delivery 2 days; capacity 193 units; certified yes.
V08-09: unit price 13; shipping 74; fixed discount 4; delivery 3 days; capacity 216 units; certified no.
V08-10: unit price 20; shipping 91; fixed discount 17; delivery 4 days; capacity 239 units; certified yes.
V08-11: unit price 12; shipping 108; fixed discount 30; delivery 5 days; capacity 82 units; certified yes.
V08-12: unit price 19; shipping 35; fixed discount 8; delivery 6 days; capacity 105 units; certified yes.
V08-13: unit price 11; shipping 52; fixed discount 21; delivery 7 days; capacity 128 units; certified no.
V08-14: unit price 18; shipping 69; fixed discount 34; delivery 1 days; capacity 151 units; certified yes.
V08-15: unit price 10; shipping 86; fixed discount 12; delivery 2 days; capacity 174 units; certified yes.
V08-16: unit price 17; shipping 103; fixed discount 25; delivery 3 days; capacity 197 units; certified yes.
V08-17: unit price 9; shipping 30; fixed discount 3; delivery 4 days; capacity 220 units; certified no.
V08-18: unit price 16; shipping 47; fixed discount 16; delivery 5 days; capacity 63 units; certified yes.
V08-19: unit price 8; shipping 64; fixed discount 29; delivery 6 days; capacity 86 units; certified yes.
V08-20: unit price 15; shipping 81; fixed discount 7; delivery 7 days; capacity 109 units; certified yes.
V08-21: unit price 22; shipping 98; fixed discount 20; delivery 1 days; capacity 132 units; certified no.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-09 / trial 9

Medium case 09: speaker decision.

Input tokens including chat template: 1020. Budget: 1024.

Reference answer: `{"vendor": "V09-02", "landed_cost": 2085, "eligible_vendors": 4, "delivery_days": 2}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M09: buy 171 speaker units in one order.
Delivery deadline: 3 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V09-01: unit price 20; shipping 39; fixed discount 10; delivery 1 days; capacity 196 units; certified yes.
V09-02: unit price 12; shipping 56; fixed discount 23; delivery 2 days; capacity 196 units; certified yes.
V09-03: unit price 19; shipping 73; fixed discount 1; delivery 5 days; capacity 97 units; certified yes.
V09-04: unit price 11; shipping 90; fixed discount 14; delivery 6 days; capacity 120 units; certified no.
V09-05: unit price 18; shipping 107; fixed discount 27; delivery 7 days; capacity 143 units; certified yes.
V09-06: unit price 10; shipping 34; fixed discount 5; delivery 1 days; capacity 166 units; certified yes.
V09-07: unit price 17; shipping 51; fixed discount 18; delivery 2 days; capacity 189 units; certified yes.
V09-08: unit price 9; shipping 68; fixed discount 31; delivery 3 days; capacity 212 units; certified no.
V09-09: unit price 16; shipping 85; fixed discount 9; delivery 4 days; capacity 235 units; certified yes.
V09-10: unit price 8; shipping 102; fixed discount 22; delivery 5 days; capacity 78 units; certified yes.
V09-11: unit price 15; shipping 119; fixed discount 0; delivery 6 days; capacity 101 units; certified yes.
V09-12: unit price 22; shipping 46; fixed discount 13; delivery 7 days; capacity 124 units; certified no.
V09-13: unit price 14; shipping 63; fixed discount 26; delivery 1 days; capacity 147 units; certified yes.
V09-14: unit price 21; shipping 80; fixed discount 4; delivery 2 days; capacity 170 units; certified yes.
V09-15: unit price 13; shipping 97; fixed discount 17; delivery 3 days; capacity 193 units; certified yes.
V09-16: unit price 20; shipping 114; fixed discount 30; delivery 4 days; capacity 216 units; certified no.
V09-17: unit price 12; shipping 41; fixed discount 8; delivery 5 days; capacity 239 units; certified yes.
V09-18: unit price 19; shipping 58; fixed discount 21; delivery 6 days; capacity 82 units; certified yes.
V09-19: unit price 11; shipping 75; fixed discount 34; delivery 7 days; capacity 105 units; certified yes.
V09-20: unit price 18; shipping 92; fixed discount 12; delivery 1 days; capacity 128 units; certified no.
V09-21: unit price 10; shipping 109; fixed discount 25; delivery 2 days; capacity 151 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Medium / medium-10 / trial 10

Medium case 10: projector decision.

Input tokens including chat template: 1019. Budget: 1024.

Reference answer: `{"vendor": "V10-01", "landed_cost": 1475, "eligible_vendors": 5, "delivery_days": 1}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement case M10: buy 180 projector units in one order.
Delivery deadline: 4 days. Prices are credits per unit.
A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.
Landed cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.
Choose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.
QUOTES:
V10-01: unit price 8; shipping 50; fixed discount 15; delivery 1 days; capacity 205 units; certified yes.
V10-02: unit price 15; shipping 67; fixed discount 28; delivery 2 days; capacity 205 units; certified yes.
V10-03: unit price 22; shipping 84; fixed discount 6; delivery 6 days; capacity 116 units; certified no.
V10-04: unit price 14; shipping 101; fixed discount 19; delivery 7 days; capacity 139 units; certified yes.
V10-05: unit price 21; shipping 118; fixed discount 32; delivery 1 days; capacity 162 units; certified yes.
V10-06: unit price 13; shipping 45; fixed discount 10; delivery 2 days; capacity 185 units; certified yes.
V10-07: unit price 20; shipping 62; fixed discount 23; delivery 3 days; capacity 208 units; certified no.
V10-08: unit price 12; shipping 79; fixed discount 1; delivery 4 days; capacity 231 units; certified yes.
V10-09: unit price 19; shipping 96; fixed discount 14; delivery 5 days; capacity 74 units; certified yes.
V10-10: unit price 11; shipping 113; fixed discount 27; delivery 6 days; capacity 97 units; certified yes.
V10-11: unit price 18; shipping 40; fixed discount 5; delivery 7 days; capacity 120 units; certified no.
V10-12: unit price 10; shipping 57; fixed discount 18; delivery 1 days; capacity 143 units; certified yes.
V10-13: unit price 17; shipping 74; fixed discount 31; delivery 2 days; capacity 166 units; certified yes.
V10-14: unit price 9; shipping 91; fixed discount 9; delivery 3 days; capacity 189 units; certified yes.
V10-15: unit price 16; shipping 108; fixed discount 22; delivery 4 days; capacity 212 units; certified no.
V10-16: unit price 8; shipping 35; fixed discount 0; delivery 5 days; capacity 235 units; certified yes.
V10-17: unit price 15; shipping 52; fixed discount 13; delivery 6 days; capacity 78 units; certified yes.
V10-18: unit price 22; shipping 69; fixed discount 26; delivery 7 days; capacity 101 units; certified yes.
V10-19: unit price 14; shipping 86; fixed discount 4; delivery 1 days; capacity 124 units; certified no.
V10-20: unit price 21; shipping 103; fixed discount 17; delivery 2 days; capacity 147 units; certified yes.
V10-21: unit price 13; shipping 30; fixed discount 30; delivery 3 days; capacity 170 units; certified yes.
Example format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.
Compute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).
```

## Long / long-01 / trial 1

Long case 01: monitor decision.

Input tokens including chat template: 4093. Budget: 4096.

Reference answer: `{"destination": "Bandung", "available_units": 226, "shortfall_units": 683, "action": "REORDER"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L01 for monitor shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=255; SBY=278; SMG=301 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-1000.
E002 | day 01, slot 2 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-1017.
E003 | day 01, slot 3 | site BDG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1034.
E004 | day 01, slot 4 | site SBY | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-1051.
E005 | day 01, slot 5 | site SMG | IN 13 units | status=posted | quality=quarantine | carrier=train | consignment=CN-1068.
E006 | day 02, slot 1 | site BDG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-1085.
E007 | day 02, slot 2 | site SBY | OUT 27 units | status=void | quality=usable | carrier=ferry | consignment=CN-1102.
E008 | day 02, slot 3 | site SMG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-1119.
E009 | day 02, slot 4 | site BDG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-1136.
E010 | day 02, slot 5 | site SBY | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-1153.
E011 | day 03, slot 1 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1170.
E012 | day 03, slot 2 | site BDG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-1187.
E013 | day 03, slot 3 | site SBY | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-1204.
E014 | day 03, slot 4 | site SMG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-1221.
E015 | day 03, slot 5 | site BDG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1238.
E016 | day 04, slot 1 | site SBY | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-1255.
E017 | day 04, slot 2 | site SMG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-1272.
E018 | day 04, slot 3 | site BDG | OUT 8 units | status=void | quality=quarantine | carrier=van | consignment=CN-1289.
E019 | day 04, slot 4 | site SBY | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1306.
E020 | day 04, slot 5 | site SMG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-1323.
E021 | day 05, slot 1 | site BDG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-1340.
E022 | day 05, slot 2 | site SBY | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-1357.
E023 | day 05, slot 3 | site SMG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1374.
E024 | day 05, slot 4 | site BDG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-1391.
E025 | day 05, slot 5 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-1408.
E026 | day 06, slot 1 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-1425.
E027 | day 06, slot 2 | site BDG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1442.
E028 | day 06, slot 3 | site SBY | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-1459.
E029 | day 06, slot 4 | site SMG | IN 13 units | status=void | quality=usable | carrier=train | consignment=CN-1476.
E030 | day 06, slot 5 | site BDG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-1493.
E031 | day 07, slot 1 | site SBY | OUT 27 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-1510.
E032 | day 07, slot 2 | site SMG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-1527.
E033 | day 07, slot 3 | site BDG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-1544.
E034 | day 07, slot 4 | site SBY | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-1561.
E035 | day 07, slot 5 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1578.
E036 | day 08, slot 1 | site BDG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-1595.
E037 | day 08, slot 2 | site SBY | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-1612.
E038 | day 08, slot 3 | site SMG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-1629.
E039 | day 08, slot 4 | site BDG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1646.
E040 | day 08, slot 5 | site SBY | IN 18 units | status=void | quality=usable | carrier=truck | consignment=CN-1663.
E041 | day 09, slot 1 | site SMG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-1680.
E042 | day 09, slot 2 | site BDG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-1697.
E043 | day 09, slot 3 | site SBY | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1714.
E044 | day 09, slot 4 | site SMG | IN 22 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-1731.
E045 | day 09, slot 5 | site BDG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-1748.
E046 | day 10, slot 1 | site SBY | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-1765.
E047 | day 10, slot 2 | site SMG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1782.
E048 | day 10, slot 3 | site BDG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-1799.
E049 | day 10, slot 4 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-1816.
E050 | day 10, slot 5 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-1833.
E051 | day 11, slot 1 | site BDG | OUT 23 units | status=void | quality=usable | carrier=ferry | consignment=CN-1850.
E052 | day 11, slot 2 | site SBY | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-1867.
E053 | day 11, slot 3 | site SMG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-1884.
E054 | day 11, slot 4 | site BDG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-1901.
E055 | day 11, slot 5 | site SBY | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1918.
E056 | day 12, slot 1 | site SMG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-1935.
E057 | day 12, slot 2 | site BDG | IN 17 units | status=posted | quality=quarantine | carrier=train | consignment=CN-1952.
E058 | day 12, slot 3 | site SBY | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-1969.
E059 | day 12, slot 4 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-1986.
E060 | day 12, slot 5 | site BDG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-2003.
E061 | day 13, slot 1 | site SBY | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-2020.
E062 | day 13, slot 2 | site SMG | OUT 4 units | status=void | quality=usable | carrier=van | consignment=CN-2037.
E063 | day 13, slot 3 | site BDG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2054.
E064 | day 13, slot 4 | site SBY | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-2071.
E065 | day 13, slot 5 | site SMG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-2088.
E066 | day 14, slot 1 | site BDG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-2105.
E067 | day 14, slot 2 | site SBY | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2122.
E068 | day 14, slot 3 | site SMG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-2139.
E069 | day 14, slot 4 | site BDG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-2156.
E070 | day 14, slot 5 | site SBY | OUT 12 units | status=posted | quality=quarantine | carrier=van | consignment=CN-2173.
E071 | day 15, slot 1 | site SMG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2190.
E072 | day 15, slot 2 | site BDG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-2207.
E073 | day 15, slot 3 | site SBY | IN 9 units | status=void | quality=usable | carrier=train | consignment=CN-2224.
E074 | day 15, slot 4 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-2241.
E075 | day 15, slot 5 | site BDG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2258.
E076 | day 16, slot 1 | site SBY | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-2275.
E077 | day 16, slot 2 | site SMG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-2292.
E078 | day 16, slot 3 | site BDG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-2309.
E079 | day 16, slot 4 | site SBY | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2326.
E080 | day 16, slot 5 | site SMG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-2343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=20 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=9 on E041; keep other fields.
Notice 4: replace units=12 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination BDG; demand 909 units; reservations 23 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-02 / trial 2

Long case 02: keyboard decision.

Input tokens including chat template: 4094. Budget: 4096.

Reference answer: `{"destination": "Surabaya", "available_units": 227, "shortfall_units": 0, "action": "RELEASE"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L02 for keyboard shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=290; SBY=313; SMG=336 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-2000.
E002 | day 01, slot 2 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2017.
E003 | day 01, slot 3 | site SBY | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-2034.
E004 | day 01, slot 4 | site SMG | IN 11 units | status=posted | quality=quarantine | carrier=train | consignment=CN-2051.
E005 | day 01, slot 5 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-2068.
E006 | day 02, slot 1 | site SBY | OUT 25 units | status=void | quality=usable | carrier=ferry | consignment=CN-2085.
E007 | day 02, slot 2 | site SMG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-2102.
E008 | day 02, slot 3 | site BDG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-2119.
E009 | day 02, slot 4 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-2136.
E010 | day 02, slot 5 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2153.
E011 | day 03, slot 1 | site BDG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-2170.
E012 | day 03, slot 2 | site SBY | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-2187.
E013 | day 03, slot 3 | site SMG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-2204.
E014 | day 03, slot 4 | site BDG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2221.
E015 | day 03, slot 5 | site SBY | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-2238.
E016 | day 04, slot 1 | site SMG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-2255.
E017 | day 04, slot 2 | site BDG | OUT 6 units | status=void | quality=quarantine | carrier=van | consignment=CN-2272.
E018 | day 04, slot 3 | site SBY | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2289.
E019 | day 04, slot 4 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-2306.
E020 | day 04, slot 5 | site BDG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-2323.
E021 | day 05, slot 1 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-2340.
E022 | day 05, slot 2 | site SMG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2357.
E023 | day 05, slot 3 | site BDG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-2374.
E024 | day 05, slot 4 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-2391.
E025 | day 05, slot 5 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-2408.
E026 | day 06, slot 1 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2425.
E027 | day 06, slot 2 | site SBY | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-2442.
E028 | day 06, slot 3 | site SMG | IN 11 units | status=void | quality=usable | carrier=train | consignment=CN-2459.
E029 | day 06, slot 4 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-2476.
E030 | day 06, slot 5 | site SBY | OUT 25 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-2493.
E031 | day 07, slot 1 | site SMG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-2510.
E032 | day 07, slot 2 | site BDG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-2527.
E033 | day 07, slot 3 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-2544.
E034 | day 07, slot 4 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2561.
E035 | day 07, slot 5 | site BDG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-2578.
E036 | day 08, slot 1 | site SBY | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-2595.
E037 | day 08, slot 2 | site SMG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-2612.
E038 | day 08, slot 3 | site BDG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2629.
E039 | day 08, slot 4 | site SBY | IN 16 units | status=void | quality=usable | carrier=truck | consignment=CN-2646.
E040 | day 08, slot 5 | site SMG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-2663.
E041 | day 09, slot 1 | site BDG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-2680.
E042 | day 09, slot 2 | site SBY | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2697.
E043 | day 09, slot 3 | site SMG | IN 20 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-2714.
E044 | day 09, slot 4 | site BDG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-2731.
E045 | day 09, slot 5 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-2748.
E046 | day 10, slot 1 | site SMG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2765.
E047 | day 10, slot 2 | site BDG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-2782.
E048 | day 10, slot 3 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-2799.
E049 | day 10, slot 4 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-2816.
E050 | day 10, slot 5 | site BDG | OUT 21 units | status=void | quality=usable | carrier=ferry | consignment=CN-2833.
E051 | day 11, slot 1 | site SBY | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-2850.
E052 | day 11, slot 2 | site SMG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-2867.
E053 | day 11, slot 3 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-2884.
E054 | day 11, slot 4 | site SBY | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2901.
E055 | day 11, slot 5 | site SMG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-2918.
E056 | day 12, slot 1 | site BDG | IN 15 units | status=posted | quality=quarantine | carrier=train | consignment=CN-2935.
E057 | day 12, slot 2 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-2952.
E058 | day 12, slot 3 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2969.
E059 | day 12, slot 4 | site BDG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-2986.
E060 | day 12, slot 5 | site SBY | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-3003.
E061 | day 13, slot 1 | site SMG | OUT 26 units | status=void | quality=usable | carrier=van | consignment=CN-3020.
E062 | day 13, slot 2 | site BDG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3037.
E063 | day 13, slot 3 | site SBY | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-3054.
E064 | day 13, slot 4 | site SMG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-3071.
E065 | day 13, slot 5 | site BDG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-3088.
E066 | day 14, slot 1 | site SBY | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3105.
E067 | day 14, slot 2 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-3122.
E068 | day 14, slot 3 | site BDG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-3139.
E069 | day 14, slot 4 | site SBY | OUT 10 units | status=posted | quality=quarantine | carrier=van | consignment=CN-3156.
E070 | day 14, slot 5 | site SMG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3173.
E071 | day 15, slot 1 | site BDG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-3190.
E072 | day 15, slot 2 | site SBY | IN 7 units | status=void | quality=usable | carrier=train | consignment=CN-3207.
E073 | day 15, slot 3 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-3224.
E074 | day 15, slot 4 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3241.
E075 | day 15, slot 5 | site SBY | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-3258.
E076 | day 16, slot 1 | site SMG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-3275.
E077 | day 16, slot 2 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-3292.
E078 | day 16, slot 3 | site SBY | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3309.
E079 | day 16, slot 4 | site SMG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-3326.
E080 | day 16, slot 5 | site BDG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-3343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=21 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=10 on E041; keep other fields.
Notice 4: replace units=13 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination SBY; demand 200 units; reservations 26 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-03 / trial 3

Long case 03: router decision.

Input tokens including chat template: 4094. Budget: 4096.

Reference answer: `{"destination": "Semarang", "available_units": 273, "shortfall_units": 654, "action": "REORDER"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L03 for router shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=325; SBY=348; SMG=371 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3000.
E002 | day 01, slot 2 | site SBY | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-3017.
E003 | day 01, slot 3 | site SMG | IN 9 units | status=posted | quality=quarantine | carrier=train | consignment=CN-3034.
E004 | day 01, slot 4 | site BDG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-3051.
E005 | day 01, slot 5 | site SBY | OUT 23 units | status=void | quality=usable | carrier=ferry | consignment=CN-3068.
E006 | day 02, slot 1 | site SMG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-3085.
E007 | day 02, slot 2 | site BDG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-3102.
E008 | day 02, slot 3 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-3119.
E009 | day 02, slot 4 | site SMG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3136.
E010 | day 02, slot 5 | site BDG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-3153.
E011 | day 03, slot 1 | site SBY | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-3170.
E012 | day 03, slot 2 | site SMG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-3187.
E013 | day 03, slot 3 | site BDG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3204.
E014 | day 03, slot 4 | site SBY | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-3221.
E015 | day 03, slot 5 | site SMG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-3238.
E016 | day 04, slot 1 | site BDG | OUT 4 units | status=void | quality=quarantine | carrier=van | consignment=CN-3255.
E017 | day 04, slot 2 | site SBY | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3272.
E018 | day 04, slot 3 | site SMG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-3289.
E019 | day 04, slot 4 | site BDG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-3306.
E020 | day 04, slot 5 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-3323.
E021 | day 05, slot 1 | site SMG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3340.
E022 | day 05, slot 2 | site BDG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-3357.
E023 | day 05, slot 3 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-3374.
E024 | day 05, slot 4 | site SMG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-3391.
E025 | day 05, slot 5 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3408.
E026 | day 06, slot 1 | site SBY | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-3425.
E027 | day 06, slot 2 | site SMG | IN 9 units | status=void | quality=usable | carrier=train | consignment=CN-3442.
E028 | day 06, slot 3 | site BDG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-3459.
E029 | day 06, slot 4 | site SBY | OUT 23 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-3476.
E030 | day 06, slot 5 | site SMG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-3493.
E031 | day 07, slot 1 | site BDG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-3510.
E032 | day 07, slot 2 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-3527.
E033 | day 07, slot 3 | site SMG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3544.
E034 | day 07, slot 4 | site BDG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-3561.
E035 | day 07, slot 5 | site SBY | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-3578.
E036 | day 08, slot 1 | site SMG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-3595.
E037 | day 08, slot 2 | site BDG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3612.
E038 | day 08, slot 3 | site SBY | IN 14 units | status=void | quality=usable | carrier=truck | consignment=CN-3629.
E039 | day 08, slot 4 | site SMG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-3646.
E040 | day 08, slot 5 | site BDG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-3663.
E041 | day 09, slot 1 | site SBY | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3680.
E042 | day 09, slot 2 | site SMG | IN 18 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-3697.
E043 | day 09, slot 3 | site BDG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-3714.
E044 | day 09, slot 4 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-3731.
E045 | day 09, slot 5 | site SMG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3748.
E046 | day 10, slot 1 | site BDG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-3765.
E047 | day 10, slot 2 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-3782.
E048 | day 10, slot 3 | site SMG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-3799.
E049 | day 10, slot 4 | site BDG | OUT 19 units | status=void | quality=usable | carrier=ferry | consignment=CN-3816.
E050 | day 10, slot 5 | site SBY | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-3833.
E051 | day 11, slot 1 | site SMG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-3850.
E052 | day 11, slot 2 | site BDG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-3867.
E053 | day 11, slot 3 | site SBY | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3884.
E054 | day 11, slot 4 | site SMG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-3901.
E055 | day 11, slot 5 | site BDG | IN 13 units | status=posted | quality=quarantine | carrier=train | consignment=CN-3918.
E056 | day 12, slot 1 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-3935.
E057 | day 12, slot 2 | site SMG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3952.
E058 | day 12, slot 3 | site BDG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-3969.
E059 | day 12, slot 4 | site SBY | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-3986.
E060 | day 12, slot 5 | site SMG | OUT 24 units | status=void | quality=usable | carrier=van | consignment=CN-4003.
E061 | day 13, slot 1 | site BDG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4020.
E062 | day 13, slot 2 | site SBY | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-4037.
E063 | day 13, slot 3 | site SMG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-4054.
E064 | day 13, slot 4 | site BDG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-4071.
E065 | day 13, slot 5 | site SBY | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4088.
E066 | day 14, slot 1 | site SMG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-4105.
E067 | day 14, slot 2 | site BDG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-4122.
E068 | day 14, slot 3 | site SBY | OUT 8 units | status=posted | quality=quarantine | carrier=van | consignment=CN-4139.
E069 | day 14, slot 4 | site SMG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4156.
E070 | day 14, slot 5 | site BDG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-4173.
E071 | day 15, slot 1 | site SBY | IN 5 units | status=void | quality=usable | carrier=train | consignment=CN-4190.
E072 | day 15, slot 2 | site SMG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-4207.
E073 | day 15, slot 3 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4224.
E074 | day 15, slot 4 | site SBY | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-4241.
E075 | day 15, slot 5 | site SMG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-4258.
E076 | day 16, slot 1 | site BDG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-4275.
E077 | day 16, slot 2 | site SBY | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4292.
E078 | day 16, slot 3 | site SMG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-4309.
E079 | day 16, slot 4 | site BDG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-4326.
E080 | day 16, slot 5 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-4343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=22 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=11 on E041; keep other fields.
Notice 4: replace units=14 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination SMG; demand 927 units; reservations 29 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-04 / trial 4

Long case 04: printer decision.

Input tokens including chat template: 4096. Budget: 4096.

Reference answer: `{"destination": "Bandung", "available_units": 371, "shortfall_units": 0, "action": "RELEASE"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L04 for printer shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=360; SBY=383; SMG=406 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SBY | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-4000.
E002 | day 01, slot 2 | site SMG | IN 7 units | status=posted | quality=quarantine | carrier=train | consignment=CN-4017.
E003 | day 01, slot 3 | site BDG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-4034.
E004 | day 01, slot 4 | site SBY | OUT 21 units | status=void | quality=usable | carrier=ferry | consignment=CN-4051.
E005 | day 01, slot 5 | site SMG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-4068.
E006 | day 02, slot 1 | site BDG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-4085.
E007 | day 02, slot 2 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-4102.
E008 | day 02, slot 3 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4119.
E009 | day 02, slot 4 | site BDG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-4136.
E010 | day 02, slot 5 | site SBY | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-4153.
E011 | day 03, slot 1 | site SMG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-4170.
E012 | day 03, slot 2 | site BDG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4187.
E013 | day 03, slot 3 | site SBY | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-4204.
E014 | day 03, slot 4 | site SMG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-4221.
E015 | day 03, slot 5 | site BDG | OUT 26 units | status=void | quality=quarantine | carrier=van | consignment=CN-4238.
E016 | day 04, slot 1 | site SBY | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4255.
E017 | day 04, slot 2 | site SMG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-4272.
E018 | day 04, slot 3 | site BDG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-4289.
E019 | day 04, slot 4 | site SBY | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-4306.
E020 | day 04, slot 5 | site SMG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4323.
E021 | day 05, slot 1 | site BDG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-4340.
E022 | day 05, slot 2 | site SBY | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-4357.
E023 | day 05, slot 3 | site SMG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-4374.
E024 | day 05, slot 4 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4391.
E025 | day 05, slot 5 | site SBY | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-4408.
E026 | day 06, slot 1 | site SMG | IN 7 units | status=void | quality=usable | carrier=train | consignment=CN-4425.
E027 | day 06, slot 2 | site BDG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-4442.
E028 | day 06, slot 3 | site SBY | OUT 21 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-4459.
E029 | day 06, slot 4 | site SMG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-4476.
E030 | day 06, slot 5 | site BDG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-4493.
E031 | day 07, slot 1 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-4510.
E032 | day 07, slot 2 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4527.
E033 | day 07, slot 3 | site BDG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-4544.
E034 | day 07, slot 4 | site SBY | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-4561.
E035 | day 07, slot 5 | site SMG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-4578.
E036 | day 08, slot 1 | site BDG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4595.
E037 | day 08, slot 2 | site SBY | IN 12 units | status=void | quality=usable | carrier=truck | consignment=CN-4612.
E038 | day 08, slot 3 | site SMG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-4629.
E039 | day 08, slot 4 | site BDG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-4646.
E040 | day 08, slot 5 | site SBY | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4663.
E041 | day 09, slot 1 | site SMG | IN 16 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-4680.
E042 | day 09, slot 2 | site BDG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-4697.
E043 | day 09, slot 3 | site SBY | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-4714.
E044 | day 09, slot 4 | site SMG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4731.
E045 | day 09, slot 5 | site BDG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-4748.
E046 | day 10, slot 1 | site SBY | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-4765.
E047 | day 10, slot 2 | site SMG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-4782.
E048 | day 10, slot 3 | site BDG | OUT 17 units | status=void | quality=usable | carrier=ferry | consignment=CN-4799.
E049 | day 10, slot 4 | site SBY | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-4816.
E050 | day 10, slot 5 | site SMG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-4833.
E051 | day 11, slot 1 | site BDG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-4850.
E052 | day 11, slot 2 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4867.
E053 | day 11, slot 3 | site SMG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-4884.
E054 | day 11, slot 4 | site BDG | IN 11 units | status=posted | quality=quarantine | carrier=train | consignment=CN-4901.
E055 | day 11, slot 5 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-4918.
E056 | day 12, slot 1 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-4935.
E057 | day 12, slot 2 | site BDG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-4952.
E058 | day 12, slot 3 | site SBY | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-4969.
E059 | day 12, slot 4 | site SMG | OUT 22 units | status=void | quality=usable | carrier=van | consignment=CN-4986.
E060 | day 12, slot 5 | site BDG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5003.
E061 | day 13, slot 1 | site SBY | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-5020.
E062 | day 13, slot 2 | site SMG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-5037.
E063 | day 13, slot 3 | site BDG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-5054.
E064 | day 13, slot 4 | site SBY | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5071.
E065 | day 13, slot 5 | site SMG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-5088.
E066 | day 14, slot 1 | site BDG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-5105.
E067 | day 14, slot 2 | site SBY | OUT 6 units | status=posted | quality=quarantine | carrier=van | consignment=CN-5122.
E068 | day 14, slot 3 | site SMG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5139.
E069 | day 14, slot 4 | site BDG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-5156.
E070 | day 14, slot 5 | site SBY | IN 27 units | status=void | quality=usable | carrier=train | consignment=CN-5173.
E071 | day 15, slot 1 | site SMG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-5190.
E072 | day 15, slot 2 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5207.
E073 | day 15, slot 3 | site SBY | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-5224.
E074 | day 15, slot 4 | site SMG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-5241.
E075 | day 15, slot 5 | site BDG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-5258.
E076 | day 16, slot 1 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5275.
E077 | day 16, slot 2 | site SMG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-5292.
E078 | day 16, slot 3 | site BDG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-5309.
E079 | day 16, slot 4 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-5326.
E080 | day 16, slot 5 | site SMG | OUT 25 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-5343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=23 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=12 on E041; keep other fields.
Notice 4: replace units=15 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination BDG; demand 210 units; reservations 32 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-05 / trial 5

Long case 05: tablet decision.

Input tokens including chat template: 4095. Budget: 4096.

Reference answer: `{"destination": "Surabaya", "available_units": 427, "shortfall_units": 518, "action": "REORDER"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L05 for tablet shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=395; SBY=418; SMG=441 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SMG | IN 5 units | status=posted | quality=quarantine | carrier=train | consignment=CN-5000.
E002 | day 01, slot 2 | site BDG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-5017.
E003 | day 01, slot 3 | site SBY | OUT 19 units | status=void | quality=usable | carrier=ferry | consignment=CN-5034.
E004 | day 01, slot 4 | site SMG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-5051.
E005 | day 01, slot 5 | site BDG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-5068.
E006 | day 02, slot 1 | site SBY | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-5085.
E007 | day 02, slot 2 | site SMG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5102.
E008 | day 02, slot 3 | site BDG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-5119.
E009 | day 02, slot 4 | site SBY | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-5136.
E010 | day 02, slot 5 | site SMG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-5153.
E011 | day 03, slot 1 | site BDG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5170.
E012 | day 03, slot 2 | site SBY | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-5187.
E013 | day 03, slot 3 | site SMG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-5204.
E014 | day 03, slot 4 | site BDG | OUT 24 units | status=void | quality=quarantine | carrier=van | consignment=CN-5221.
E015 | day 03, slot 5 | site SBY | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5238.
E016 | day 04, slot 1 | site SMG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-5255.
E017 | day 04, slot 2 | site BDG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-5272.
E018 | day 04, slot 3 | site SBY | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-5289.
E019 | day 04, slot 4 | site SMG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5306.
E020 | day 04, slot 5 | site BDG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-5323.
E021 | day 05, slot 1 | site SBY | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-5340.
E022 | day 05, slot 2 | site SMG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-5357.
E023 | day 05, slot 3 | site BDG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5374.
E024 | day 05, slot 4 | site SBY | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-5391.
E025 | day 05, slot 5 | site SMG | IN 5 units | status=void | quality=usable | carrier=train | consignment=CN-5408.
E026 | day 06, slot 1 | site BDG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-5425.
E027 | day 06, slot 2 | site SBY | OUT 19 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-5442.
E028 | day 06, slot 3 | site SMG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-5459.
E029 | day 06, slot 4 | site BDG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-5476.
E030 | day 06, slot 5 | site SBY | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-5493.
E031 | day 07, slot 1 | site SMG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5510.
E032 | day 07, slot 2 | site BDG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-5527.
E033 | day 07, slot 3 | site SBY | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-5544.
E034 | day 07, slot 4 | site SMG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-5561.
E035 | day 07, slot 5 | site BDG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5578.
E036 | day 08, slot 1 | site SBY | IN 10 units | status=void | quality=usable | carrier=truck | consignment=CN-5595.
E037 | day 08, slot 2 | site SMG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-5612.
E038 | day 08, slot 3 | site BDG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-5629.
E039 | day 08, slot 4 | site SBY | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5646.
E040 | day 08, slot 5 | site SMG | IN 14 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-5663.
E041 | day 09, slot 1 | site BDG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-5680.
E042 | day 09, slot 2 | site SBY | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-5697.
E043 | day 09, slot 3 | site SMG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5714.
E044 | day 09, slot 4 | site BDG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-5731.
E045 | day 09, slot 5 | site SBY | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-5748.
E046 | day 10, slot 1 | site SMG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-5765.
E047 | day 10, slot 2 | site BDG | OUT 15 units | status=void | quality=usable | carrier=ferry | consignment=CN-5782.
E048 | day 10, slot 3 | site SBY | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-5799.
E049 | day 10, slot 4 | site SMG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-5816.
E050 | day 10, slot 5 | site BDG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-5833.
E051 | day 11, slot 1 | site SBY | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5850.
E052 | day 11, slot 2 | site SMG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-5867.
E053 | day 11, slot 3 | site BDG | IN 9 units | status=posted | quality=quarantine | carrier=train | consignment=CN-5884.
E054 | day 11, slot 4 | site SBY | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-5901.
E055 | day 11, slot 5 | site SMG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5918.
E056 | day 12, slot 1 | site BDG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-5935.
E057 | day 12, slot 2 | site SBY | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-5952.
E058 | day 12, slot 3 | site SMG | OUT 20 units | status=void | quality=usable | carrier=van | consignment=CN-5969.
E059 | day 12, slot 4 | site BDG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-5986.
E060 | day 12, slot 5 | site SBY | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-6003.
E061 | day 13, slot 1 | site SMG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-6020.
E062 | day 13, slot 2 | site BDG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-6037.
E063 | day 13, slot 3 | site SBY | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6054.
E064 | day 13, slot 4 | site SMG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-6071.
E065 | day 13, slot 5 | site BDG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-6088.
E066 | day 14, slot 1 | site SBY | OUT 4 units | status=posted | quality=quarantine | carrier=van | consignment=CN-6105.
E067 | day 14, slot 2 | site SMG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6122.
E068 | day 14, slot 3 | site BDG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-6139.
E069 | day 14, slot 4 | site SBY | IN 25 units | status=void | quality=usable | carrier=train | consignment=CN-6156.
E070 | day 14, slot 5 | site SMG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-6173.
E071 | day 15, slot 1 | site BDG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6190.
E072 | day 15, slot 2 | site SBY | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-6207.
E073 | day 15, slot 3 | site SMG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-6224.
E074 | day 15, slot 4 | site BDG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-6241.
E075 | day 15, slot 5 | site SBY | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6258.
E076 | day 16, slot 1 | site SMG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-6275.
E077 | day 16, slot 2 | site BDG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-6292.
E078 | day 16, slot 3 | site SBY | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-6309.
E079 | day 16, slot 4 | site SMG | OUT 23 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-6326.
E080 | day 16, slot 5 | site BDG | IN 6 units | status=void | quality=usable | carrier=truck | consignment=CN-6343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=24 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=13 on E041; keep other fields.
Notice 4: replace units=16 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination SBY; demand 945 units; reservations 35 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-06 / trial 6

Long case 06: scanner decision.

Input tokens including chat template: 4094. Budget: 4096.

Reference answer: `{"destination": "Semarang", "available_units": 489, "shortfall_units": 0, "action": "RELEASE"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L06 for scanner shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=430; SBY=453; SMG=476 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site BDG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-6000.
E002 | day 01, slot 2 | site SBY | OUT 17 units | status=void | quality=usable | carrier=ferry | consignment=CN-6017.
E003 | day 01, slot 3 | site SMG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-6034.
E004 | day 01, slot 4 | site BDG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-6051.
E005 | day 01, slot 5 | site SBY | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-6068.
E006 | day 02, slot 1 | site SMG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6085.
E007 | day 02, slot 2 | site BDG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-6102.
E008 | day 02, slot 3 | site SBY | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-6119.
E009 | day 02, slot 4 | site SMG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-6136.
E010 | day 02, slot 5 | site BDG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6153.
E011 | day 03, slot 1 | site SBY | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-6170.
E012 | day 03, slot 2 | site SMG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-6187.
E013 | day 03, slot 3 | site BDG | OUT 22 units | status=void | quality=quarantine | carrier=van | consignment=CN-6204.
E014 | day 03, slot 4 | site SBY | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6221.
E015 | day 03, slot 5 | site SMG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-6238.
E016 | day 04, slot 1 | site BDG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-6255.
E017 | day 04, slot 2 | site SBY | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-6272.
E018 | day 04, slot 3 | site SMG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6289.
E019 | day 04, slot 4 | site BDG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-6306.
E020 | day 04, slot 5 | site SBY | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-6323.
E021 | day 05, slot 1 | site SMG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-6340.
E022 | day 05, slot 2 | site BDG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6357.
E023 | day 05, slot 3 | site SBY | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-6374.
E024 | day 05, slot 4 | site SMG | IN 27 units | status=void | quality=usable | carrier=train | consignment=CN-6391.
E025 | day 05, slot 5 | site BDG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-6408.
E026 | day 06, slot 1 | site SBY | OUT 17 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-6425.
E027 | day 06, slot 2 | site SMG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-6442.
E028 | day 06, slot 3 | site BDG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-6459.
E029 | day 06, slot 4 | site SBY | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-6476.
E030 | day 06, slot 5 | site SMG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6493.
E031 | day 07, slot 1 | site BDG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-6510.
E032 | day 07, slot 2 | site SBY | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-6527.
E033 | day 07, slot 3 | site SMG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-6544.
E034 | day 07, slot 4 | site BDG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6561.
E035 | day 07, slot 5 | site SBY | IN 8 units | status=void | quality=usable | carrier=truck | consignment=CN-6578.
E036 | day 08, slot 1 | site SMG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-6595.
E037 | day 08, slot 2 | site BDG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-6612.
E038 | day 08, slot 3 | site SBY | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6629.
E039 | day 08, slot 4 | site SMG | IN 12 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-6646.
E040 | day 08, slot 5 | site BDG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-6663.
E041 | day 09, slot 1 | site SBY | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-6680.
E042 | day 09, slot 2 | site SMG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6697.
E043 | day 09, slot 3 | site BDG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-6714.
E044 | day 09, slot 4 | site SBY | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-6731.
E045 | day 09, slot 5 | site SMG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-6748.
E046 | day 10, slot 1 | site BDG | OUT 13 units | status=void | quality=usable | carrier=ferry | consignment=CN-6765.
E047 | day 10, slot 2 | site SBY | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-6782.
E048 | day 10, slot 3 | site SMG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-6799.
E049 | day 10, slot 4 | site BDG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-6816.
E050 | day 10, slot 5 | site SBY | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6833.
E051 | day 11, slot 1 | site SMG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-6850.
E052 | day 11, slot 2 | site BDG | IN 7 units | status=posted | quality=quarantine | carrier=train | consignment=CN-6867.
E053 | day 11, slot 3 | site SBY | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-6884.
E054 | day 11, slot 4 | site SMG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6901.
E055 | day 11, slot 5 | site BDG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-6918.
E056 | day 12, slot 1 | site SBY | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-6935.
E057 | day 12, slot 2 | site SMG | OUT 18 units | status=void | quality=usable | carrier=van | consignment=CN-6952.
E058 | day 12, slot 3 | site BDG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-6969.
E059 | day 12, slot 4 | site SBY | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-6986.
E060 | day 12, slot 5 | site SMG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-7003.
E061 | day 13, slot 1 | site BDG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-7020.
E062 | day 13, slot 2 | site SBY | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7037.
E063 | day 13, slot 3 | site SMG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-7054.
E064 | day 13, slot 4 | site BDG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-7071.
E065 | day 13, slot 5 | site SBY | OUT 26 units | status=posted | quality=quarantine | carrier=van | consignment=CN-7088.
E066 | day 14, slot 1 | site SMG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7105.
E067 | day 14, slot 2 | site BDG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-7122.
E068 | day 14, slot 3 | site SBY | IN 23 units | status=void | quality=usable | carrier=train | consignment=CN-7139.
E069 | day 14, slot 4 | site SMG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-7156.
E070 | day 14, slot 5 | site BDG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7173.
E071 | day 15, slot 1 | site SBY | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-7190.
E072 | day 15, slot 2 | site SMG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-7207.
E073 | day 15, slot 3 | site BDG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-7224.
E074 | day 15, slot 4 | site SBY | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7241.
E075 | day 15, slot 5 | site SMG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-7258.
E076 | day 16, slot 1 | site BDG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-7275.
E077 | day 16, slot 2 | site SBY | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-7292.
E078 | day 16, slot 3 | site SMG | OUT 21 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-7309.
E079 | day 16, slot 4 | site BDG | IN 4 units | status=void | quality=usable | carrier=truck | consignment=CN-7326.
E080 | day 16, slot 5 | site SBY | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-7343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=25 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=14 on E041; keep other fields.
Notice 4: replace units=17 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination SMG; demand 220 units; reservations 38 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-07 / trial 7

Long case 07: webcam decision.

Input tokens including chat template: 4094. Budget: 4096.

Reference answer: `{"destination": "Bandung", "available_units": 450, "shortfall_units": 513, "action": "REORDER"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L07 for webcam shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=465; SBY=488; SMG=511 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SBY | OUT 15 units | status=void | quality=usable | carrier=ferry | consignment=CN-7000.
E002 | day 01, slot 2 | site SMG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-7017.
E003 | day 01, slot 3 | site BDG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-7034.
E004 | day 01, slot 4 | site SBY | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-7051.
E005 | day 01, slot 5 | site SMG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7068.
E006 | day 02, slot 1 | site BDG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-7085.
E007 | day 02, slot 2 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-7102.
E008 | day 02, slot 3 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-7119.
E009 | day 02, slot 4 | site BDG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7136.
E010 | day 02, slot 5 | site SBY | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-7153.
E011 | day 03, slot 1 | site SMG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-7170.
E012 | day 03, slot 2 | site BDG | OUT 20 units | status=void | quality=quarantine | carrier=van | consignment=CN-7187.
E013 | day 03, slot 3 | site SBY | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7204.
E014 | day 03, slot 4 | site SMG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-7221.
E015 | day 03, slot 5 | site BDG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-7238.
E016 | day 04, slot 1 | site SBY | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-7255.
E017 | day 04, slot 2 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7272.
E018 | day 04, slot 3 | site BDG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-7289.
E019 | day 04, slot 4 | site SBY | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-7306.
E020 | day 04, slot 5 | site SMG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-7323.
E021 | day 05, slot 1 | site BDG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7340.
E022 | day 05, slot 2 | site SBY | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-7357.
E023 | day 05, slot 3 | site SMG | IN 25 units | status=void | quality=usable | carrier=train | consignment=CN-7374.
E024 | day 05, slot 4 | site BDG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-7391.
E025 | day 05, slot 5 | site SBY | OUT 15 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-7408.
E026 | day 06, slot 1 | site SMG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-7425.
E027 | day 06, slot 2 | site BDG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-7442.
E028 | day 06, slot 3 | site SBY | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-7459.
E029 | day 06, slot 4 | site SMG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7476.
E030 | day 06, slot 5 | site BDG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-7493.
E031 | day 07, slot 1 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-7510.
E032 | day 07, slot 2 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-7527.
E033 | day 07, slot 3 | site BDG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7544.
E034 | day 07, slot 4 | site SBY | IN 6 units | status=void | quality=usable | carrier=truck | consignment=CN-7561.
E035 | day 07, slot 5 | site SMG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-7578.
E036 | day 08, slot 1 | site BDG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-7595.
E037 | day 08, slot 2 | site SBY | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7612.
E038 | day 08, slot 3 | site SMG | IN 10 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-7629.
E039 | day 08, slot 4 | site BDG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-7646.
E040 | day 08, slot 5 | site SBY | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-7663.
E041 | day 09, slot 1 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7680.
E042 | day 09, slot 2 | site BDG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-7697.
E043 | day 09, slot 3 | site SBY | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-7714.
E044 | day 09, slot 4 | site SMG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-7731.
E045 | day 09, slot 5 | site BDG | OUT 11 units | status=void | quality=usable | carrier=ferry | consignment=CN-7748.
E046 | day 10, slot 1 | site SBY | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-7765.
E047 | day 10, slot 2 | site SMG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-7782.
E048 | day 10, slot 3 | site BDG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-7799.
E049 | day 10, slot 4 | site SBY | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7816.
E050 | day 10, slot 5 | site SMG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-7833.
E051 | day 11, slot 1 | site BDG | IN 5 units | status=posted | quality=quarantine | carrier=train | consignment=CN-7850.
E052 | day 11, slot 2 | site SBY | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-7867.
E053 | day 11, slot 3 | site SMG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7884.
E054 | day 11, slot 4 | site BDG | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-7901.
E055 | day 11, slot 5 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-7918.
E056 | day 12, slot 1 | site SMG | OUT 16 units | status=void | quality=usable | carrier=van | consignment=CN-7935.
E057 | day 12, slot 2 | site BDG | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-7952.
E058 | day 12, slot 3 | site SBY | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-7969.
E059 | day 12, slot 4 | site SMG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-7986.
E060 | day 12, slot 5 | site BDG | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-8003.
E061 | day 13, slot 1 | site SBY | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8020.
E062 | day 13, slot 2 | site SMG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-8037.
E063 | day 13, slot 3 | site BDG | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-8054.
E064 | day 13, slot 4 | site SBY | OUT 24 units | status=posted | quality=quarantine | carrier=van | consignment=CN-8071.
E065 | day 13, slot 5 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8088.
E066 | day 14, slot 1 | site BDG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-8105.
E067 | day 14, slot 2 | site SBY | IN 21 units | status=void | quality=usable | carrier=train | consignment=CN-8122.
E068 | day 14, slot 3 | site SMG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-8139.
E069 | day 14, slot 4 | site BDG | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8156.
E070 | day 14, slot 5 | site SBY | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-8173.
E071 | day 15, slot 1 | site SMG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-8190.
E072 | day 15, slot 2 | site BDG | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-8207.
E073 | day 15, slot 3 | site SBY | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8224.
E074 | day 15, slot 4 | site SMG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-8241.
E075 | day 15, slot 5 | site BDG | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-8258.
E076 | day 16, slot 1 | site SBY | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-8275.
E077 | day 16, slot 2 | site SMG | OUT 19 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-8292.
E078 | day 16, slot 3 | site BDG | IN 26 units | status=void | quality=usable | carrier=truck | consignment=CN-8309.
E079 | day 16, slot 4 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-8326.
E080 | day 16, slot 5 | site SMG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-8343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=26 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=15 on E041; keep other fields.
Notice 4: replace units=18 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination BDG; demand 963 units; reservations 41 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-08 / trial 8

Long case 08: headset decision.

Input tokens including chat template: 4095. Budget: 4096.

Reference answer: `{"destination": "Surabaya", "available_units": 426, "shortfall_units": 0, "action": "RELEASE"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L08 for headset shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=500; SBY=523; SMG=546 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-8000.
E002 | day 01, slot 2 | site BDG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-8017.
E003 | day 01, slot 3 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-8034.
E004 | day 01, slot 4 | site SMG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8051.
E005 | day 01, slot 5 | site BDG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-8068.
E006 | day 02, slot 1 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-8085.
E007 | day 02, slot 2 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-8102.
E008 | day 02, slot 3 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8119.
E009 | day 02, slot 4 | site SBY | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-8136.
E010 | day 02, slot 5 | site SMG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-8153.
E011 | day 03, slot 1 | site BDG | OUT 18 units | status=void | quality=quarantine | carrier=van | consignment=CN-8170.
E012 | day 03, slot 2 | site SBY | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8187.
E013 | day 03, slot 3 | site SMG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-8204.
E014 | day 03, slot 4 | site BDG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-8221.
E015 | day 03, slot 5 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-8238.
E016 | day 04, slot 1 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8255.
E017 | day 04, slot 2 | site BDG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-8272.
E018 | day 04, slot 3 | site SBY | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-8289.
E019 | day 04, slot 4 | site SMG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-8306.
E020 | day 04, slot 5 | site BDG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8323.
E021 | day 05, slot 1 | site SBY | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-8340.
E022 | day 05, slot 2 | site SMG | IN 23 units | status=void | quality=usable | carrier=train | consignment=CN-8357.
E023 | day 05, slot 3 | site BDG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-8374.
E024 | day 05, slot 4 | site SBY | OUT 13 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-8391.
E025 | day 05, slot 5 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-8408.
E026 | day 06, slot 1 | site BDG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-8425.
E027 | day 06, slot 2 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-8442.
E028 | day 06, slot 3 | site SMG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8459.
E029 | day 06, slot 4 | site BDG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-8476.
E030 | day 06, slot 5 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-8493.
E031 | day 07, slot 1 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-8510.
E032 | day 07, slot 2 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8527.
E033 | day 07, slot 3 | site SBY | IN 4 units | status=void | quality=usable | carrier=truck | consignment=CN-8544.
E034 | day 07, slot 4 | site SMG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-8561.
E035 | day 07, slot 5 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-8578.
E036 | day 08, slot 1 | site SBY | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8595.
E037 | day 08, slot 2 | site SMG | IN 8 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-8612.
E038 | day 08, slot 3 | site BDG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-8629.
E039 | day 08, slot 4 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-8646.
E040 | day 08, slot 5 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8663.
E041 | day 09, slot 1 | site BDG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-8680.
E042 | day 09, slot 2 | site SBY | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-8697.
E043 | day 09, slot 3 | site SMG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-8714.
E044 | day 09, slot 4 | site BDG | OUT 9 units | status=void | quality=usable | carrier=ferry | consignment=CN-8731.
E045 | day 09, slot 5 | site SBY | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-8748.
E046 | day 10, slot 1 | site SMG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-8765.
E047 | day 10, slot 2 | site BDG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-8782.
E048 | day 10, slot 3 | site SBY | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8799.
E049 | day 10, slot 4 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-8816.
E050 | day 10, slot 5 | site BDG | IN 27 units | status=posted | quality=quarantine | carrier=train | consignment=CN-8833.
E051 | day 11, slot 1 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-8850.
E052 | day 11, slot 2 | site SMG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8867.
E053 | day 11, slot 3 | site BDG | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-8884.
E054 | day 11, slot 4 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-8901.
E055 | day 11, slot 5 | site SMG | OUT 14 units | status=void | quality=usable | carrier=van | consignment=CN-8918.
E056 | day 12, slot 1 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-8935.
E057 | day 12, slot 2 | site SBY | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-8952.
E058 | day 12, slot 3 | site SMG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-8969.
E059 | day 12, slot 4 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-8986.
E060 | day 12, slot 5 | site SBY | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9003.
E061 | day 13, slot 1 | site SMG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-9020.
E062 | day 13, slot 2 | site BDG | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-9037.
E063 | day 13, slot 3 | site SBY | OUT 22 units | status=posted | quality=quarantine | carrier=van | consignment=CN-9054.
E064 | day 13, slot 4 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9071.
E065 | day 13, slot 5 | site BDG | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-9088.
E066 | day 14, slot 1 | site SBY | IN 19 units | status=void | quality=usable | carrier=train | consignment=CN-9105.
E067 | day 14, slot 2 | site SMG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-9122.
E068 | day 14, slot 3 | site BDG | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9139.
E069 | day 14, slot 4 | site SBY | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-9156.
E070 | day 14, slot 5 | site SMG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-9173.
E071 | day 15, slot 1 | site BDG | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-9190.
E072 | day 15, slot 2 | site SBY | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9207.
E073 | day 15, slot 3 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-9224.
E074 | day 15, slot 4 | site BDG | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-9241.
E075 | day 15, slot 5 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-9258.
E076 | day 16, slot 1 | site SMG | OUT 17 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-9275.
E077 | day 16, slot 2 | site BDG | IN 24 units | status=void | quality=usable | carrier=truck | consignment=CN-9292.
E078 | day 16, slot 3 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-9309.
E079 | day 16, slot 4 | site SMG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-9326.
E080 | day 16, slot 5 | site BDG | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9343.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=27 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=16 on E041; keep other fields.
Notice 4: replace units=19 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination SBY; demand 230 units; reservations 44 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-09 / trial 9

Long case 09: speaker decision.

Input tokens including chat template: 4068. Budget: 4096.

Reference answer: `{"destination": "Semarang", "available_units": 450, "shortfall_units": 531, "action": "REORDER"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L09 for speaker shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=535; SBY=558; SMG=581 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site BDG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-9000.
E002 | day 01, slot 2 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-9017.
E003 | day 01, slot 3 | site SMG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9034.
E004 | day 01, slot 4 | site BDG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-9051.
E005 | day 01, slot 5 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-9068.
E006 | day 02, slot 1 | site SMG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-9085.
E007 | day 02, slot 2 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9102.
E008 | day 02, slot 3 | site SBY | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-9119.
E009 | day 02, slot 4 | site SMG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-9136.
E010 | day 02, slot 5 | site BDG | OUT 16 units | status=void | quality=quarantine | carrier=van | consignment=CN-9153.
E011 | day 03, slot 1 | site SBY | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9170.
E012 | day 03, slot 2 | site SMG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-9187.
E013 | day 03, slot 3 | site BDG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-9204.
E014 | day 03, slot 4 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-9221.
E015 | day 03, slot 5 | site SMG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9238.
E016 | day 04, slot 1 | site BDG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-9255.
E017 | day 04, slot 2 | site SBY | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-9272.
E018 | day 04, slot 3 | site SMG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-9289.
E019 | day 04, slot 4 | site BDG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9306.
E020 | day 04, slot 5 | site SBY | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-9323.
E021 | day 05, slot 1 | site SMG | IN 21 units | status=void | quality=usable | carrier=train | consignment=CN-9340.
E022 | day 05, slot 2 | site BDG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-9357.
E023 | day 05, slot 3 | site SBY | OUT 11 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-9374.
E024 | day 05, slot 4 | site SMG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-9391.
E025 | day 05, slot 5 | site BDG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-9408.
E026 | day 06, slot 1 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-9425.
E027 | day 06, slot 2 | site SMG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9442.
E028 | day 06, slot 3 | site BDG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-9459.
E029 | day 06, slot 4 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-9476.
E030 | day 06, slot 5 | site SMG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-9493.
E031 | day 07, slot 1 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9510.
E032 | day 07, slot 2 | site SBY | IN 26 units | status=void | quality=usable | carrier=truck | consignment=CN-9527.
E033 | day 07, slot 3 | site SMG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-9544.
E034 | day 07, slot 4 | site BDG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-9561.
E035 | day 07, slot 5 | site SBY | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9578.
E036 | day 08, slot 1 | site SMG | IN 6 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-9595.
E037 | day 08, slot 2 | site BDG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-9612.
E038 | day 08, slot 3 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=van | consignment=CN-9629.
E039 | day 08, slot 4 | site SMG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9646.
E040 | day 08, slot 5 | site BDG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-9663.
E041 | day 09, slot 1 | site SBY | IN 17 units | status=posted | quality=usable | carrier=train | consignment=CN-9680.
E042 | day 09, slot 2 | site SMG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-9697.
E043 | day 09, slot 3 | site BDG | OUT 7 units | status=void | quality=usable | carrier=ferry | consignment=CN-9714.
E044 | day 09, slot 4 | site SBY | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-9731.
E045 | day 09, slot 5 | site SMG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-9748.
E046 | day 10, slot 1 | site BDG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-9765.
E047 | day 10, slot 2 | site SBY | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9782.
E048 | day 10, slot 3 | site SMG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-9799.
E049 | day 10, slot 4 | site BDG | IN 25 units | status=posted | quality=quarantine | carrier=train | consignment=CN-9816.
E050 | day 10, slot 5 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-9833.
E051 | day 11, slot 1 | site SMG | OUT 15 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9850.
E052 | day 11, slot 2 | site BDG | IN 22 units | status=posted | quality=usable | carrier=truck | consignment=CN-9867.
E053 | day 11, slot 3 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-9884.
E054 | day 11, slot 4 | site SMG | OUT 12 units | status=void | quality=usable | carrier=van | consignment=CN-9901.
E055 | day 11, slot 5 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9918.
E056 | day 12, slot 1 | site SBY | IN 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-9935.
E057 | day 12, slot 2 | site SMG | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-9952.
E058 | day 12, slot 3 | site BDG | OUT 16 units | status=posted | quality=usable | carrier=van | consignment=CN-9969.
E059 | day 12, slot 4 | site SBY | OUT 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-9986.
E060 | day 12, slot 5 | site SMG | IN 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-10003.
E061 | day 13, slot 1 | site BDG | IN 13 units | status=posted | quality=usable | carrier=train | consignment=CN-10020.
E062 | day 13, slot 2 | site SBY | OUT 20 units | status=posted | quality=quarantine | carrier=van | consignment=CN-10037.
E063 | day 13, slot 3 | site SMG | OUT 27 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10054.
E064 | day 13, slot 4 | site BDG | IN 10 units | status=posted | quality=usable | carrier=truck | consignment=CN-10071.
E065 | day 13, slot 5 | site SBY | IN 17 units | status=void | quality=usable | carrier=train | consignment=CN-10088.
E066 | day 14, slot 1 | site SMG | OUT 24 units | status=posted | quality=usable | carrier=van | consignment=CN-10105.
E067 | day 14, slot 2 | site BDG | OUT 7 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10122.
E068 | day 14, slot 3 | site SBY | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-10139.
E069 | day 14, slot 4 | site SMG | IN 21 units | status=posted | quality=usable | carrier=train | consignment=CN-10156.
E070 | day 14, slot 5 | site BDG | OUT 4 units | status=posted | quality=usable | carrier=van | consignment=CN-10173.
E071 | day 15, slot 1 | site SBY | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10190.
E072 | day 15, slot 2 | site SMG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-10207.
E073 | day 15, slot 3 | site BDG | IN 25 units | status=posted | quality=usable | carrier=train | consignment=CN-10224.
E074 | day 15, slot 4 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=van | consignment=CN-10241.
E075 | day 15, slot 5 | site SMG | OUT 15 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-10258.
E076 | day 16, slot 1 | site BDG | IN 22 units | status=void | quality=usable | carrier=truck | consignment=CN-10275.
E077 | day 16, slot 2 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-10292.
E078 | day 16, slot 3 | site SMG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-10309.
E079 | day 16, slot 4 | site BDG | OUT 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10326.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=28 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=17 on E040; keep other fields.
Notice 4: replace units=20 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination SMG; demand 981 units; reservations 47 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```

## Long / long-10 / trial 10

Long case 10: projector decision.

Input tokens including chat template: 4082. Budget: 4096.

Reference answer: `{"destination": "Bandung", "available_units": 479, "shortfall_units": 0, "action": "RELEASE"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Dispatch reconciliation L10 for projector shipments.
DOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.
DOCUMENT C - Opening usable stock: BDG=570; SBY=593; SMG=616 units.
At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.
IDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.
DOCUMENT D - Movement register:
E001 | day 01, slot 1 | site SBY | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-10000.
E002 | day 01, slot 2 | site SMG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10017.
E003 | day 01, slot 3 | site BDG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-10034.
E004 | day 01, slot 4 | site SBY | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-10051.
E005 | day 01, slot 5 | site SMG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-10068.
E006 | day 02, slot 1 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10085.
E007 | day 02, slot 2 | site SBY | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-10102.
E008 | day 02, slot 3 | site SMG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-10119.
E009 | day 02, slot 4 | site BDG | OUT 14 units | status=void | quality=quarantine | carrier=van | consignment=CN-10136.
E010 | day 02, slot 5 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10153.
E011 | day 03, slot 1 | site SMG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-10170.
E012 | day 03, slot 2 | site BDG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-10187.
E013 | day 03, slot 3 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-10204.
E014 | day 03, slot 4 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10221.
E015 | day 03, slot 5 | site BDG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-10238.
E016 | day 04, slot 1 | site SBY | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-10255.
E017 | day 04, slot 2 | site SMG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-10272.
E018 | day 04, slot 3 | site BDG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10289.
E019 | day 04, slot 4 | site SBY | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-10306.
E020 | day 04, slot 5 | site SMG | IN 19 units | status=void | quality=usable | carrier=train | consignment=CN-10323.
E021 | day 05, slot 1 | site BDG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-10340.
E022 | day 05, slot 2 | site SBY | OUT 9 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-10357.
E023 | day 05, slot 3 | site SMG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-10374.
E024 | day 05, slot 4 | site BDG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-10391.
E025 | day 05, slot 5 | site SBY | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-10408.
E026 | day 06, slot 1 | site SMG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10425.
E027 | day 06, slot 2 | site BDG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-10442.
E028 | day 06, slot 3 | site SBY | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-10459.
E029 | day 06, slot 4 | site SMG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-10476.
E030 | day 06, slot 5 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10493.
E031 | day 07, slot 1 | site SBY | IN 24 units | status=void | quality=usable | carrier=truck | consignment=CN-10510.
E032 | day 07, slot 2 | site SMG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-10527.
E033 | day 07, slot 3 | site BDG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-10544.
E034 | day 07, slot 4 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10561.
E035 | day 07, slot 5 | site SMG | IN 4 units | status=posted | quality=quarantine | carrier=truck | consignment=CN-10578.
E036 | day 08, slot 1 | site BDG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-10595.
E037 | day 08, slot 2 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-10612.
E038 | day 08, slot 3 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10629.
E039 | day 08, slot 4 | site BDG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-10646.
E040 | day 08, slot 5 | site SBY | IN 15 units | status=posted | quality=usable | carrier=train | consignment=CN-10663.
E041 | day 09, slot 1 | site SMG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-10680.
E042 | day 09, slot 2 | site BDG | OUT 5 units | status=void | quality=usable | carrier=ferry | consignment=CN-10697.
E043 | day 09, slot 3 | site SBY | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-10714.
E044 | day 09, slot 4 | site SMG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-10731.
E045 | day 09, slot 5 | site BDG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-10748.
E046 | day 10, slot 1 | site SBY | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10765.
E047 | day 10, slot 2 | site SMG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-10782.
E048 | day 10, slot 3 | site BDG | IN 23 units | status=posted | quality=quarantine | carrier=train | consignment=CN-10799.
E049 | day 10, slot 4 | site SBY | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-10816.
E050 | day 10, slot 5 | site SMG | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10833.
E051 | day 11, slot 1 | site BDG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-10850.
E052 | day 11, slot 2 | site SBY | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-10867.
E053 | day 11, slot 3 | site SMG | OUT 10 units | status=void | quality=usable | carrier=van | consignment=CN-10884.
E054 | day 11, slot 4 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10901.
E055 | day 11, slot 5 | site SBY | IN 24 units | status=posted | quality=usable | carrier=truck | consignment=CN-10918.
E056 | day 12, slot 1 | site SMG | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-10935.
E057 | day 12, slot 2 | site BDG | OUT 14 units | status=posted | quality=usable | carrier=van | consignment=CN-10952.
E058 | day 12, slot 3 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-10969.
E059 | day 12, slot 4 | site SMG | IN 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-10986.
E060 | day 12, slot 5 | site BDG | IN 11 units | status=posted | quality=usable | carrier=train | consignment=CN-11003.
E061 | day 13, slot 1 | site SBY | OUT 18 units | status=posted | quality=quarantine | carrier=van | consignment=CN-11020.
E062 | day 13, slot 2 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-11037.
E063 | day 13, slot 3 | site BDG | IN 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-11054.
E064 | day 13, slot 4 | site SBY | IN 15 units | status=void | quality=usable | carrier=train | consignment=CN-11071.
E065 | day 13, slot 5 | site SMG | OUT 22 units | status=posted | quality=usable | carrier=van | consignment=CN-11088.
E066 | day 14, slot 1 | site BDG | OUT 5 units | status=posted | quality=usable | carrier=ferry | consignment=CN-11105.
E067 | day 14, slot 2 | site SBY | IN 12 units | status=posted | quality=usable | carrier=truck | consignment=CN-11122.
E068 | day 14, slot 3 | site SMG | IN 19 units | status=posted | quality=usable | carrier=train | consignment=CN-11139.
E069 | day 14, slot 4 | site BDG | OUT 26 units | status=posted | quality=usable | carrier=van | consignment=CN-11156.
E070 | day 14, slot 5 | site SBY | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-11173.
E071 | day 15, slot 1 | site SMG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-11190.
E072 | day 15, slot 2 | site BDG | IN 23 units | status=posted | quality=usable | carrier=train | consignment=CN-11207.
E073 | day 15, slot 3 | site SBY | OUT 6 units | status=posted | quality=usable | carrier=van | consignment=CN-11224.
E074 | day 15, slot 4 | site SMG | OUT 13 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-11241.
E075 | day 15, slot 5 | site BDG | IN 20 units | status=void | quality=usable | carrier=truck | consignment=CN-11258.
E076 | day 16, slot 1 | site SBY | IN 27 units | status=posted | quality=usable | carrier=train | consignment=CN-11275.
E077 | day 16, slot 2 | site SMG | OUT 10 units | status=posted | quality=usable | carrier=van | consignment=CN-11292.
E078 | day 16, slot 3 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=ferry | consignment=CN-11309.
DOCUMENT E - Correction notices, in this order:
Notice 1: replace units=29 on E001; keep other fields.
Notice 2: replace status=void on E003; keep other fields.
Notice 3: replace units=18 on E040; keep other fields.
Notice 4: replace units=21 on E001; keep other fields.
DOCUMENT F - Final memo, version 2: destination BDG; demand 240 units; reservations 50 units. This controls the dispatch. Opening stock remains Document C.
Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.
Example format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.
Compute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).
```
