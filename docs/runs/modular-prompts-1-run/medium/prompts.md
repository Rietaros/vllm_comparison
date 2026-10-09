# Complete benchmark prompts

Suite: editable-prompts-and-expectations-v4

System message: Use only the supplied data. Apply every stated rule and return the requested JSON.

## Short

Single-item stock arithmetic and a fulfillment decision.

Input tokens including chat template: 256. Unique records: 9.

Reference answer: `{"item": "MONITOR", "available_units": 68, "fulfillable": true}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Stock check for item MONITOR at the Bandung shop.
Opening stock is zero. Every receipt below was accepted and is a separate delivery.
Receipt R01: 17 units.
Receipt R02: 25 units.
Receipt R03: 2 units.
Receipt R04: 5 units.
Receipt R05: 8 units.
Receipt R06: 4 units.
Receipt R07: 7 units.
Receipt R08: 3 units.
Receipt R09: 6 units.
Already reserved: 9 units. A new customer requests 40 units.
Available stock = accepted receipts minus existing reservations.
Example JSON format only (illustrative values, not the answer):
{"item": "PENCIL", "available_units": 5, "fulfillable": false}
Calculate your actual values from the data. Return integer results, not arithmetic expressions.
Return JSON only with exactly these keys: "item" (the item name only), "available_units" (integer), "fulfillable" (boolean: available stock >= the new request).
```

## Medium

Filter competing quotes, calculate landed costs and rank eligible suppliers.

Input tokens including chat template: 992. Unique records: 20.

Reference answer: `{"vendor": "TAMBORA", "landed_cost": 1365, "eligible_vendors": 7, "delivery_days": 4}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Procurement decision: purchase 120 routers, paid in credits.
A supplier is eligible only when certified, able to supply all 120 units, and able to deliver within 4 days.
Landed cost = 120 * unit price + one shipping fee - one fixed discount. There is no tax.
Among eligible suppliers choose the lowest landed cost. Ties: fewer delivery days, then alphabetically smallest name.
Quotes are independent offers; do not add offers together or split the order.
MERAPI: unit price 12; shipping 80; fixed discount 20; delivery 3 days; capacity 150 units; certified yes.
BROMO: unit price 10; shipping 70; fixed discount 0; delivery 6 days; capacity 160 units; certified yes.
RINJANI: unit price 9; shipping 90; fixed discount 10; delivery 2 days; capacity 90 units; certified yes.
TAMBORA: unit price 11; shipping 60; fixed discount 15; delivery 4 days; capacity 140 units; certified yes.
SUPPLIER-01: unit price 11; shipping 35; fixed discount 0; delivery 2 days; capacity 80 units; certified yes.
SUPPLIER-02: unit price 16; shipping 48; fixed discount 7; delivery 3 days; capacity 97 units; certified no.
SUPPLIER-03: unit price 12; shipping 61; fixed discount 14; delivery 4 days; capacity 114 units; certified yes.
SUPPLIER-04: unit price 17; shipping 74; fixed discount 21; delivery 5 days; capacity 131 units; certified yes.
SUPPLIER-05: unit price 13; shipping 87; fixed discount 28; delivery 6 days; capacity 148 units; certified yes.
SUPPLIER-06: unit price 18; shipping 100; fixed discount 35; delivery 7 days; capacity 165 units; certified no.
SUPPLIER-07: unit price 14; shipping 113; fixed discount 2; delivery 2 days; capacity 182 units; certified yes.
SUPPLIER-08: unit price 19; shipping 126; fixed discount 9; delivery 3 days; capacity 199 units; certified yes.
SUPPLIER-09: unit price 15; shipping 39; fixed discount 16; delivery 4 days; capacity 216 units; certified yes.
SUPPLIER-10: unit price 11; shipping 52; fixed discount 23; delivery 5 days; capacity 93 units; certified no.
SUPPLIER-11: unit price 16; shipping 65; fixed discount 30; delivery 6 days; capacity 110 units; certified yes.
SUPPLIER-12: unit price 12; shipping 78; fixed discount 37; delivery 7 days; capacity 127 units; certified yes.
SUPPLIER-13: unit price 17; shipping 91; fixed discount 4; delivery 2 days; capacity 144 units; certified yes.
SUPPLIER-14: unit price 13; shipping 104; fixed discount 11; delivery 3 days; capacity 161 units; certified no.
SUPPLIER-15: unit price 18; shipping 117; fixed discount 18; delivery 4 days; capacity 178 units; certified yes.
SUPPLIER-16: unit price 14; shipping 130; fixed discount 25; delivery 5 days; capacity 195 units; certified yes.
Example JSON format only (illustrative values, not the answer):
{"vendor": "EXAMPLE", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
Calculate your actual values from the data. Return integer results, not arithmetic expressions.
Return JSON only with exactly these keys: "vendor" (winning name exactly as shown), "landed_cost" (integer credits), "eligible_vendors" (integer count), "delivery_days" (integer for the winner).
```

## Long

Reconcile a multi-document ledger, apply corrections and the latest policy, then calculate a dispatch decision.

Input tokens including chat template: 4065. Unique records: 77.

Reference answer: `{"destination": "Surabaya", "available_units": 215, "shortfall_units": 205, "action": "REORDER"}`.

Comparison rules: `{"allow_extra_fields": false, "case_sensitive": true}`.

```text
Shipment reconciliation dossier: final dispatch decision for the school equipment program.
DOCUMENT A - Site directory: BDG means Bandung; SBY means Surabaya; SMG means Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350 units; reservations 20 units. This memo is superseded in full by Document F. Do not combine both versions.
DOCUMENT C - Stock policy: Opening usable balances before these events are BDG=210, SBY=300, SMG=180 units.
For the final destination only, apply each event once. IN adds units; OUT subtracts units. Count only status=posted AND quality=usable. Ignore void events and quarantine quantities, including quarantine OUT events.
Event IDs are unique movements; carrier and consignment references are audit metadata. Correction notices replace only specified fields on the original event. Keep unspecified fields. If multiple notices affect the same field, the last notice wins. Notices are not additional movements.
DOCUMENT D - Chronological movement register:
E001 | day 01, slot 1 | site SBY | IN 4 units | status=posted | quality=usable | carrier=train | consignment=CN-2100.
E002 | day 01, slot 2 | site BDG | OUT 11 units | status=posted | quality=usable | carrier=van | consignment=CN-2117.
E003 | day 01, slot 3 | site SBY | IN 18 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2134.
E004 | day 01, slot 4 | site SMG | OUT 25 units | status=posted | quality=usable | carrier=truck | consignment=CN-2151.
E005 | day 01, slot 5 | site SBY | IN 9 units | status=posted | quality=usable | carrier=courier | consignment=CN-2168.
E006 | day 02, slot 1 | site SBY | OUT 16 units | status=posted | quality=quarantine | carrier=train | consignment=CN-2185.
E007 | day 02, slot 2 | site BDG | IN 23 units | status=posted | quality=usable | carrier=van | consignment=CN-2202.
E008 | day 02, slot 3 | site SBY | OUT 7 units | status=void | quality=usable | carrier=ferry | consignment=CN-2219.
E009 | day 02, slot 4 | site SMG | IN 14 units | status=posted | quality=usable | carrier=truck | consignment=CN-2236.
E010 | day 02, slot 5 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=courier | consignment=CN-2253.
E011 | day 03, slot 1 | site SBY | IN 5 units | status=posted | quality=usable | carrier=train | consignment=CN-2270.
E012 | day 03, slot 2 | site BDG | OUT 12 units | status=posted | quality=usable | carrier=van | consignment=CN-2287.
E013 | day 03, slot 3 | site SBY | IN 19 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2304.
E014 | day 03, slot 4 | site SMG | OUT 26 units | status=posted | quality=usable | carrier=truck | consignment=CN-2321.
E015 | day 03, slot 5 | site SBY | IN 10 units | status=posted | quality=usable | carrier=courier | consignment=CN-2338.
E016 | day 04, slot 1 | site SBY | OUT 17 units | status=posted | quality=usable | carrier=train | consignment=CN-2355.
E017 | day 04, slot 2 | site BDG | IN 24 units | status=posted | quality=usable | carrier=van | consignment=CN-2372.
E018 | day 04, slot 3 | site SBY | OUT 8 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2389.
E019 | day 04, slot 4 | site SMG | IN 15 units | status=void | quality=quarantine | carrier=truck | consignment=CN-2406.
E020 | day 04, slot 5 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=courier | consignment=CN-2423.
E021 | day 05, slot 1 | site SBY | IN 6 units | status=posted | quality=usable | carrier=train | consignment=CN-2440.
E022 | day 05, slot 2 | site BDG | OUT 13 units | status=posted | quality=usable | carrier=van | consignment=CN-2457.
E023 | day 05, slot 3 | site SBY | IN 20 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2474.
E024 | day 05, slot 4 | site SMG | OUT 4 units | status=posted | quality=usable | carrier=truck | consignment=CN-2491.
E025 | day 05, slot 5 | site SBY | IN 11 units | status=posted | quality=usable | carrier=courier | consignment=CN-2508.
E026 | day 06, slot 1 | site SBY | OUT 18 units | status=posted | quality=usable | carrier=train | consignment=CN-2525.
E027 | day 06, slot 2 | site BDG | IN 25 units | status=posted | quality=usable | carrier=van | consignment=CN-2542.
E028 | day 06, slot 3 | site SBY | OUT 9 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2559.
E029 | day 06, slot 4 | site SMG | IN 16 units | status=posted | quality=usable | carrier=truck | consignment=CN-2576.
E030 | day 06, slot 5 | site SBY | OUT 23 units | status=void | quality=usable | carrier=courier | consignment=CN-2593.
E031 | day 07, slot 1 | site SBY | IN 7 units | status=posted | quality=usable | carrier=train | consignment=CN-2610.
E032 | day 07, slot 2 | site BDG | OUT 14 units | status=posted | quality=quarantine | carrier=van | consignment=CN-2627.
E033 | day 07, slot 3 | site SBY | IN 21 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2644.
E034 | day 07, slot 4 | site SMG | OUT 5 units | status=posted | quality=usable | carrier=truck | consignment=CN-2661.
E035 | day 07, slot 5 | site SBY | IN 12 units | status=posted | quality=usable | carrier=courier | consignment=CN-2678.
E036 | day 08, slot 1 | site SBY | OUT 19 units | status=posted | quality=usable | carrier=train | consignment=CN-2695.
E037 | day 08, slot 2 | site BDG | IN 26 units | status=posted | quality=usable | carrier=van | consignment=CN-2712.
E038 | day 08, slot 3 | site SBY | OUT 10 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2729.
E039 | day 08, slot 4 | site SMG | IN 17 units | status=posted | quality=usable | carrier=truck | consignment=CN-2746.
E040 | day 08, slot 5 | site SBY | OUT 24 units | status=posted | quality=usable | carrier=courier | consignment=CN-2763.
E041 | day 09, slot 1 | site SBY | IN 8 units | status=void | quality=usable | carrier=train | consignment=CN-2780.
E042 | day 09, slot 2 | site BDG | OUT 15 units | status=posted | quality=usable | carrier=van | consignment=CN-2797.
E043 | day 09, slot 3 | site SBY | IN 22 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2814.
E044 | day 09, slot 4 | site SMG | OUT 6 units | status=posted | quality=usable | carrier=truck | consignment=CN-2831.
E045 | day 09, slot 5 | site SBY | IN 13 units | status=posted | quality=quarantine | carrier=courier | consignment=CN-2848.
E046 | day 10, slot 1 | site SBY | OUT 20 units | status=posted | quality=usable | carrier=train | consignment=CN-2865.
E047 | day 10, slot 2 | site BDG | IN 4 units | status=posted | quality=usable | carrier=van | consignment=CN-2882.
E048 | day 10, slot 3 | site SBY | OUT 11 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2899.
E049 | day 10, slot 4 | site SMG | IN 18 units | status=posted | quality=usable | carrier=truck | consignment=CN-2916.
E050 | day 10, slot 5 | site SBY | OUT 25 units | status=posted | quality=usable | carrier=courier | consignment=CN-2933.
E051 | day 11, slot 1 | site SBY | IN 9 units | status=posted | quality=usable | carrier=train | consignment=CN-2950.
E052 | day 11, slot 2 | site BDG | OUT 16 units | status=void | quality=usable | carrier=van | consignment=CN-2967.
E053 | day 11, slot 3 | site SBY | IN 23 units | status=posted | quality=usable | carrier=ferry | consignment=CN-2984.
E054 | day 11, slot 4 | site SMG | OUT 7 units | status=posted | quality=usable | carrier=truck | consignment=CN-3001.
E055 | day 11, slot 5 | site SBY | IN 14 units | status=posted | quality=usable | carrier=courier | consignment=CN-3018.
E056 | day 12, slot 1 | site SBY | OUT 21 units | status=posted | quality=usable | carrier=train | consignment=CN-3035.
E057 | day 12, slot 2 | site BDG | IN 5 units | status=posted | quality=usable | carrier=van | consignment=CN-3052.
E058 | day 12, slot 3 | site SBY | OUT 12 units | status=posted | quality=quarantine | carrier=ferry | consignment=CN-3069.
E059 | day 12, slot 4 | site SMG | IN 19 units | status=posted | quality=usable | carrier=truck | consignment=CN-3086.
E060 | day 12, slot 5 | site SBY | OUT 26 units | status=posted | quality=usable | carrier=courier | consignment=CN-3103.
E061 | day 13, slot 1 | site SBY | IN 10 units | status=posted | quality=usable | carrier=train | consignment=CN-3120.
E062 | day 13, slot 2 | site BDG | OUT 17 units | status=posted | quality=usable | carrier=van | consignment=CN-3137.
E063 | day 13, slot 3 | site SBY | IN 24 units | status=void | quality=usable | carrier=ferry | consignment=CN-3154.
E064 | day 13, slot 4 | site SMG | OUT 8 units | status=posted | quality=usable | carrier=truck | consignment=CN-3171.
E065 | day 13, slot 5 | site SBY | IN 15 units | status=posted | quality=usable | carrier=courier | consignment=CN-3188.
E066 | day 14, slot 1 | site SBY | OUT 22 units | status=posted | quality=usable | carrier=train | consignment=CN-3205.
E067 | day 14, slot 2 | site BDG | IN 6 units | status=posted | quality=usable | carrier=van | consignment=CN-3222.
E068 | day 14, slot 3 | site SBY | OUT 13 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3239.
E069 | day 14, slot 4 | site SMG | IN 20 units | status=posted | quality=usable | carrier=truck | consignment=CN-3256.
E070 | day 14, slot 5 | site SBY | OUT 4 units | status=posted | quality=usable | carrier=courier | consignment=CN-3273.
E071 | day 15, slot 1 | site SBY | IN 11 units | status=posted | quality=quarantine | carrier=train | consignment=CN-3290.
E072 | day 15, slot 2 | site BDG | OUT 18 units | status=posted | quality=usable | carrier=van | consignment=CN-3307.
E073 | day 15, slot 3 | site SBY | IN 25 units | status=posted | quality=usable | carrier=ferry | consignment=CN-3324.
E074 | day 15, slot 4 | site SMG | OUT 9 units | status=void | quality=usable | carrier=truck | consignment=CN-3341.
E075 | day 15, slot 5 | site SBY | IN 16 units | status=posted | quality=usable | carrier=courier | consignment=CN-3358.
E076 | day 16, slot 1 | site SBY | OUT 23 units | status=posted | quality=usable | carrier=train | consignment=CN-3375.
E077 | day 16, slot 2 | site BDG | IN 7 units | status=posted | quality=usable | carrier=van | consignment=CN-3392.
DOCUMENT E - Correction notices, in authoritative order:
Notice 1: replace units=19 on E001; all other fields stay unchanged.
Notice 2: replace status=void on E003; all other fields stay unchanged.
Notice 3: replace units=8 on E039; all other fields stay unchanged.
Notice 4: replace units=11 on E001; all other fields stay unchanged.
DOCUMENT F - Final memo, version 2: destination SBY; demand 420 units; reservations 37 units. This is the controlling memo. Opening stock remains the balance in Document C.
DECISION RULE: available units = corrected usable closing balance at the final destination minus final reservations. Shortfall = max(0, final demand minus available units). Action is REORDER if shortfall > 0, otherwise RELEASE.
Example JSON format only (illustrative values, not the answer):
{"destination": "Example City", "available_units": 50, "shortfall_units": 25, "action": "REORDER"}
Calculate your actual values from the data. Return integer results, not arithmetic expressions.
Return JSON only with exactly these keys: "destination" (full city name from the directory), "available_units" (integer), "shortfall_units" (integer), "action" (REORDER or RELEASE).
```
