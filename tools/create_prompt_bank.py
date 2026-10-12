"""Recreate the initial 30 editable static cases; run manually, never during inference."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ("MONITOR", "KEYBOARD", "ROUTER", "PRINTER", "TABLET", "SCANNER", "WEBCAM", "HEADSET", "SPEAKER", "PROJECTOR")


def short_case(index, extra=0):
    item = ITEMS[index - 1]
    opening, reserved = 12 + 11 * index, 3 + 2 * index
    requested = 32 + 5 * index if index % 2 else 170 + 15 * index
    receipts = [(f"R{index:02d}{n + 1:02d}", 3 + (index * 7 + n * 5) % 19) for n in range(2 + extra)]
    available = opening + sum(units for _, units in receipts) - reserved
    text = f"Inventory decision for {item} at shop S{index:02d}.\nOpening usable stock: {opening} units.\nAll receipts below are accepted, separate deliveries:\n"
    text += "\n".join(f"Receipt {name}: {units} units." for name, units in receipts)
    text += f"\nExisting reservations: {reserved} units. New customer request: {requested} units.\nAvailable stock = opening stock + all accepted receipts - existing reservations.\nFulfillable means available stock is at least the new customer request.\n"
    text += 'Example format only: {"item":"EXAMPLE","available_units":5,"fulfillable":false}.\nCalculate from the actual data. Return JSON only with exactly "item" (item name), "available_units" (integer), and "fulfillable" (boolean).'
    return text, {"item": item, "available_units": available, "fulfillable": available >= requested}


def medium_case(index, extra=0):
    units, deadline = 90 + index * 9, 3 + index % 3
    quotes = []
    for n in range(4 + extra):
        quotes.append({"vendor": f"V{index:02d}-{n + 1:02d}", "price": 8 + (index * 3 + n * 7) % 15,
            "shipping": 30 + (index * 11 + n * 17) % 90, "discount": (index * 5 + n * 13) % 35,
            "days": (1 + n % deadline) if n < 2 else 1 + (index + n) % 7,
            "capacity": units + 25 if n < 2 else 60 + (index * 19 + n * 23) % 180,
            "certified": True if n < 2 else (index + n) % 4 != 0})
    eligible = [q for q in quotes if q["certified"] and q["capacity"] >= units and q["days"] <= deadline]
    cost = lambda q: units * q["price"] + q["shipping"] - q["discount"]
    winner = min(eligible, key=lambda q: (cost(q), q["days"], q["vendor"]))
    text = f"Procurement case M{index:02d}: buy {units} {ITEMS[index - 1].lower()} units in one order.\nDelivery deadline: {deadline} days. Prices are credits per unit.\n"
    text += "A quote is eligible only when certified, with capacity for the entire order, and delivery within the deadline.\nLanded cost = order quantity * unit price + one shipping fee - one fixed discount. No tax.\nChoose the lowest eligible cost. Break ties by fewer delivery days, then alphabetically smallest vendor name. Do not split the order.\nQUOTES:\n"
    text += "\n".join(f"{q['vendor']}: unit price {q['price']}; shipping {q['shipping']}; fixed discount {q['discount']}; delivery {q['days']} days; capacity {q['capacity']} units; certified {'yes' if q['certified'] else 'no'}." for q in quotes)
    text += '\nExample format only: {"vendor":"EXAMPLE","landed_cost":1500,"eligible_vendors":2,"delivery_days":3}.\nCompute the actual answer. Return JSON only with exactly "vendor" (winning name), "landed_cost" (integer), "eligible_vendors" (integer count), and "delivery_days" (integer).'
    return text, {"vendor": winner["vendor"], "landed_cost": cost(winner), "eligible_vendors": len(eligible), "delivery_days": winner["days"]}


def long_case(index, extra=0):
    sites = {"BDG": "Bandung", "SBY": "Surabaya", "SMG": "Semarang"}
    destination = tuple(sites)[(index - 1) % 3]
    openings = {site: 220 + 35 * index + n * 23 for n, site in enumerate(sites)}
    demand, reserved = (900 + index * 9 if index % 2 else 190 + index * 5), 20 + index * 3
    events = [{"id": f"E{n + 1:03d}", "site": tuple(sites)[(n + index) % 3],
        "operation": "IN" if (n + index) % 4 < 2 else "OUT", "units": 4 + (index * 5 + n * 7) % 24,
        "status": "void" if (n + index) % 11 == 7 else "posted",
        "quality": "quarantine" if (n + index) % 13 == 5 else "usable",
        "carrier": ("truck", "train", "van", "ferry")[(n + index) % 4], "reference": f"CN-{index * 1000 + n * 17}"}
        for n in range(12 + extra)]
    patches = [{"id": "E001", "units": 19 + index}, {"id": "E003", "status": "void"},
               {"id": events[len(events) // 2]["id"], "units": 8 + index}, {"id": "E001", "units": 11 + index}]
    reconciled = {row["id"]: dict(row) for row in events}
    for patch in patches:
        reconciled[patch["id"]].update(patch)
    available = openings[destination] - reserved
    for row in reconciled.values():
        if row["site"] == destination and row["status"] == "posted" and row["quality"] == "usable":
            available += row["units"] if row["operation"] == "IN" else -row["units"]
    shortfall = max(0, demand - available)
    text = f"Dispatch reconciliation L{index:02d} for {ITEMS[index - 1].lower()} shipments.\nDOCUMENT A - Site directory: BDG=Bandung, SBY=Surabaya, SMG=Semarang.\n"
    text += "DOCUMENT B - Initial memo, version 1: destination BDG; demand 350; reservations 20. Document F replaces this memo in full. Do not combine versions.\n"
    text += "DOCUMENT C - Opening usable stock: " + "; ".join(f"{site}={units}" for site, units in openings.items()) + " units.\n"
    text += "At the final destination, IN adds units and OUT subtracts units. Only posted AND usable events count. Ignore void and quarantine events, including quarantine OUT events.\nIDs identify separate movements. Carrier and consignment are audit metadata. Notices replace only named fields; keep other fields. The last notice for a field wins. Notices do not add movements.\nDOCUMENT D - Movement register:\n"
    text += "\n".join(f"{row['id']} | day {1 + n // 5:02d}, slot {1 + n % 5} | site {row['site']} | {row['operation']} {row['units']} units | status={row['status']} | quality={row['quality']} | carrier={row['carrier']} | consignment={row['reference']}." for n, row in enumerate(events))
    text += "\nDOCUMENT E - Correction notices, in this order:\n"
    text += "\n".join(f"Notice {n}: replace " + ", ".join(f"{key}={value}" for key, value in patch.items() if key != "id") + f" on {patch['id']}; keep other fields." for n, patch in enumerate(patches, 1))
    text += f"\nDOCUMENT F - Final memo, version 2: destination {destination}; demand {demand} units; reservations {reserved} units. This controls the dispatch. Opening stock remains Document C.\n"
    text += 'Available = corrected usable closing stock at the final destination - final reservations. Shortfall = max(0, final demand - available). Use REORDER when shortfall > 0, otherwise RELEASE.\nExample format only: {"destination":"Example City","available_units":50,"shortfall_units":25,"action":"REORDER"}.\nCompute actual values. Return JSON only with exactly "destination" (full city name), "available_units" (integer), "shortfall_units" (integer), and "action" (REORDER or RELEASE).'
    return text, {"destination": sites[destination], "available_units": available, "shortfall_units": shortfall, "action": "REORDER" if shortfall else "RELEASE"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", required=True, help="Unquantized model ID or local tokenizer folder")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "prompts")
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=False)
    system = (ROOT / "prompts/system.md").read_text().rstrip()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "system.md").write_text(system + "\n")
    manifest = {"version": 1, "system": "system.md", "contexts": {}}
    for context, directory, builder, budget, reasoning in (
        ("Short", "short", short_case, 256, ["available_units", "fulfillable"]),
        ("Medium", "medium", medium_case, 1024, ["landed_cost", "eligible_vendors", "delivery_days"]),
        ("Long", "long", long_case, 4096, ["available_units", "shortfall_units", "action"])):
        manifest["contexts"][context] = []
        (args.output_dir / directory).mkdir(exist_ok=True)
        expected_values = set()
        for index in range(1, 11):
            def tokens(text):
                return len(tokenizer.apply_chat_template([{"role": "system", "content": system}, {"role": "user", "content": text}],
                    tokenize=True, add_generation_prompt=True, enable_thinking=False, return_dict=False))
            extra = 0
            text, expected = builder(index, extra)
            if tokens(text) > budget:
                raise ValueError(f"{context}/{index:02d}: minimum case exceeds token budget")
            while tokens(builder(index, extra + 1)[0]) <= budget:
                extra += 1
            text, expected = builder(index, extra)
            canonical = json.dumps(expected, sort_keys=True)
            if canonical in expected_values:
                raise ValueError(f"Duplicate expected answer: {context}/{index}")
            expected_values.add(canonical)
            case_id = f"{directory}-{index:02d}"
            prompt_file, answer_file = f"{directory}/{index:02d}.md", f"{directory}/{index:02d}.json"
            (args.output_dir / prompt_file).write_text(text + "\n")
            (args.output_dir / answer_file).write_text(json.dumps({"mode": "static", "task_id": case_id,
                "description": f"{context} case {index:02d}: {ITEMS[index - 1].lower()} decision.",
                "expected": expected, "reasoning_fields": reasoning,
                "comparison": {"allow_extra_fields": False, "case_sensitive": True}}, indent=2) + "\n")
            manifest["contexts"][context].append({"id": case_id, "prompt": prompt_file, "expected": answer_file})
            print(case_id, tokens(text), "tokens", json.dumps(expected))
    (args.output_dir / "cases.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
