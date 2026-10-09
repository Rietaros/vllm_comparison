"""Deterministic, distinct workloads with reference answers derived from their data."""
from __future__ import annotations

import json
from pathlib import Path
from string import Template

PROMPT_SUITE = "differentiated-json-examples-v3"
PROMPT_DIR = Path(__file__).resolve().parent / "prompts"


def read_prompt(name):
    path = PROMPT_DIR / (name + ".md")
    text = path.read_text(encoding="utf-8").rstrip("\r\n")
    if not text.strip():
        raise ValueError(f"Prompt template is empty: {path}")
    return text


def render_prompt(name, **values):
    """Fill Markdown templates without interpreting their literal JSON braces."""
    template = Template(read_prompt(name))
    record_field = {"short": "receipts", "normal": "quotes", "long": "events"}[name]
    fields = {match.group("named") or match.group("braced")
              for match in template.pattern.finditer(template.template)}
    if record_field not in fields:
        raise ValueError(f"{name}.md must include ${record_field} so context fitting can add records")
    try:
        return template.substitute(values)
    except (KeyError, ValueError) as error:
        raise ValueError(f"Invalid placeholder in {name}.md: {error}") from error


SYSTEM = read_prompt("system")


def short_task(extra_records=0):
    receipts = [{"id": "R01", "units": 17}, {"id": "R02", "units": 25}]
    receipts += [{"id": f"R{i + 3:02d}", "units": 2 + (i * 3) % 7} for i in range(extra_records)]
    item, reserved, requested = "MONITOR", 9, 40
    example = {"item": "PENCIL", "available_units": 5, "fulfillable": False}
    available = sum(row["units"] for row in receipts) - reserved
    prompt = render_prompt("short", item=item, reserved=reserved, requested=requested,
                           receipts="\n".join(f"Receipt {row['id']}: {row['units']} units." for row in receipts),
                           output_example=json.dumps(example, ensure_ascii=False))
    return {"task_id": "stock-availability", "task_description": "Single-item stock arithmetic and a fulfillment decision.",
            "prompt": prompt, "record_count": len(receipts),
            "output_example": example,
            "task_data": {"item": item, "receipts": receipts, "reserved": reserved, "requested": requested},
            "expected": {"item": item, "available_units": available, "fulfillable": available >= requested},
            "reasoning_fields": ["available_units", "fulfillable"]}


def medium_task(extra_records=0):
    example = {"vendor": "EXAMPLE", "landed_cost": 1500, "eligible_vendors": 2, "delivery_days": 3}
    vendors = [
        {"vendor": "MERAPI", "unit_price": 12, "shipping": 80, "discount": 20, "days": 3, "capacity": 150, "certified": True},
        {"vendor": "BROMO", "unit_price": 10, "shipping": 70, "discount": 0, "days": 6, "capacity": 160, "certified": True},
        {"vendor": "RINJANI", "unit_price": 9, "shipping": 90, "discount": 10, "days": 2, "capacity": 90, "certified": True},
        {"vendor": "TAMBORA", "unit_price": 11, "shipping": 60, "discount": 15, "days": 4, "capacity": 140, "certified": True},
    ]
    vendors += [{"vendor": f"SUPPLIER-{i + 1:02d}", "unit_price": 11 + (i * 5) % 9,
                 "shipping": 35 + (i * 13) % 100, "discount": (i * 7) % 40,
                 "days": 2 + i % 6, "capacity": 80 + (i * 17) % 140, "certified": i % 4 != 1}
                for i in range(extra_records)]
    units, deadline = 120, 4
    eligible = [v for v in vendors if v["certified"] and v["capacity"] >= units and v["days"] <= deadline]
    cost = lambda v: units * v["unit_price"] + v["shipping"] - v["discount"]
    winner = min(eligible, key=lambda v: (cost(v), v["days"], v["vendor"]))
    quotes = "\n".join(
        f"{v['vendor']}: unit price {v['unit_price']}; shipping {v['shipping']}; fixed discount {v['discount']}; "
        f"delivery {v['days']} days; capacity {v['capacity']} units; certified {'yes' if v['certified'] else 'no'}."
        for v in vendors)
    prompt = render_prompt("normal", order_units=units, deadline_days=deadline, quotes=quotes,
                           output_example=json.dumps(example, ensure_ascii=False))
    return {"task_id": "supplier-selection", "task_description": "Filter competing quotes, calculate landed costs and rank eligible suppliers.",
            "prompt": prompt, "record_count": len(vendors),
            "output_example": example,
            "task_data": {"quotes": vendors, "order_units": units, "deadline_days": deadline},
            "expected": {"vendor": winner["vendor"], "landed_cost": cost(winner),
                         "eligible_vendors": len(eligible), "delivery_days": winner["days"]},
            "reasoning_fields": ["landed_cost", "eligible_vendors", "delivery_days"]}


def long_task(extra_records=0):
    example = {"destination": "Example City", "available_units": 50, "shortfall_units": 25, "action": "REORDER"}
    sites = {"BDG": "Bandung", "SBY": "Surabaya", "SMG": "Semarang"}
    carriers = ("train", "van", "ferry", "truck", "courier")
    events = []
    for i in range(12 + extra_records):
        events.append({"id": f"E{i + 1:03d}", "site": ("SBY", "BDG", "SBY", "SMG", "SBY")[i % 5],
                       "operation": ("IN", "OUT", "IN", "OUT")[i % 4], "units": 4 + (i * 7) % 23,
                       "status": "void" if i % 11 == 7 else "posted",
                       "quality": "quarantine" if i % 13 == 5 else "usable",
                       "carrier": carriers[i % len(carriers)], "reference": f"CN-{2100 + i * 17}"})
    # Corrections are separated from their original records and replace values,
    # rather than adding movements. E001 is deliberately corrected twice.
    patches = [{"id": "E001", "units": 19}, {"id": "E003", "status": "void"},
               {"id": events[len(events) // 2]["id"], "units": 8}, {"id": "E001", "units": 11}]
    reconciled = {row["id"]: dict(row) for row in events}
    for patch in patches:
        reconciled[patch["id"]].update(patch)
    opening, reserved, demand = 300, 37, 420
    balance = opening
    for row in reconciled.values():
        if row["site"] == "SBY" and row["status"] == "posted" and row["quality"] == "usable":
            balance += row["units"] * (1 if row["operation"] == "IN" else -1)
    available = balance - reserved
    shortfall = max(0, demand - available)
    event_lines = "\n".join(
        f"{row['id']} | day {1 + i // 5:02d}, slot {1 + i % 5} | site {row['site']} | "
        f"{row['operation']} {row['units']} units | status={row['status']} | quality={row['quality']} | "
        f"carrier={row['carrier']} | consignment={row['reference']}."
        for i, row in enumerate(events))
    corrections = []
    for i, patch in enumerate(patches, 1):
        changed = ", ".join(f"{key}={value}" for key, value in patch.items() if key != "id")
        corrections.append(f"Notice {i}: replace {changed} on {patch['id']}; all other fields stay unchanged.")
    prompt = render_prompt("long", events=event_lines, corrections="\n".join(corrections),
                           final_site="SBY", opening_units=opening, demand_units=demand, reserved_units=reserved,
                           output_example=json.dumps(example, ensure_ascii=False))
    return {"task_id": "shipment-reconciliation", "task_description": "Reconcile a multi-document ledger, apply corrections and the latest policy, then calculate a dispatch decision.",
            "prompt": prompt, "record_count": len(events),
            "output_example": example,
            "task_data": {"sites": sites, "events": events, "corrections": patches, "final_site": "SBY",
                          "opening_units": opening, "reserved_units": reserved, "demand_units": demand},
            "expected": {"destination": sites["SBY"], "available_units": available,
                         "shortfall_units": shortfall, "action": "REORDER" if shortfall else "RELEASE"},
            "reasoning_fields": ["available_units", "shortfall_units", "action"]}


TASK_BUILDERS = {"Short": short_task, "Medium": medium_task, "Long": long_task}
