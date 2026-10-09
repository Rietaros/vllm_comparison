Shipment reconciliation dossier: final dispatch decision for the school equipment program.
DOCUMENT A - Site directory: BDG means Bandung; SBY means Surabaya; SMG means Semarang.
DOCUMENT B - Initial memo, version 1: destination BDG; demand 350 units; reservations 20 units. This memo is superseded in full by Document F. Do not combine both versions.
DOCUMENT C - Stock policy: Opening usable balances before these events are BDG=210, SBY=$opening_units, SMG=180 units.
For the final destination only, apply each event once. IN adds units; OUT subtracts units. Count only status=posted AND quality=usable. Ignore void events and quarantine quantities, including quarantine OUT events.
Event IDs are unique movements; carrier and consignment references are audit metadata. Correction notices replace only specified fields on the original event. Keep unspecified fields. If multiple notices affect the same field, the last notice wins. Notices are not additional movements.
DOCUMENT D - Chronological movement register:
$events
DOCUMENT E - Correction notices, in authoritative order:
$corrections
DOCUMENT F - Final memo, version 2: destination $final_site; demand $demand_units units; reservations $reserved_units units. This is the controlling memo. Opening stock remains the balance in Document C.
DECISION RULE: available units = corrected usable closing balance at the final destination minus final reservations. Shortfall = max(0, final demand minus available units). Action is REORDER if shortfall > 0, otherwise RELEASE.
Example JSON format only (illustrative values, not the answer):
$output_example
Calculate your actual values from the data. Return integer results, not arithmetic expressions.
Return JSON only with exactly these keys: "destination" (full city name from the directory), "available_units" (integer), "shortfall_units" (integer), "action" (REORDER or RELEASE).
