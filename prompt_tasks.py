"""Deterministic, distinct workloads with reference answers derived from their data."""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
from string import Template

from answer_comparison import comparison_options, validate_expected

PROMPT_SUITE = "editable-prompts-and-expectations-v4"
PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
TASK_NAMES = {"Short": "short", "Medium": "normal", "Long": "long"}


def task_suite_sha256():
    """Include answers and scoring rules, even when prompt token IDs do not change."""
    digest = hashlib.sha256()
    for name in ("system.md", *(name + suffix for name in TASK_NAMES.values() for suffix in (".md", ".json"))):
        content = (PROMPT_DIR / name).read_bytes()
        digest.update(name.encode() + b"\0" + len(content).to_bytes(8, "big") + content)
    return digest.hexdigest()


def load_expectation(name):
    path = PROMPT_DIR / (name + ".json")
    try:
        definition = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error
    allowed = {"mode", "task_id", "description", "expected", "reasoning_fields", "output_example", "comparison"}
    if not isinstance(definition, dict) or set(definition) - allowed:
        raise ValueError(f"Unsupported task configuration in {path}; allowed keys: {', '.join(sorted(allowed))}")
    if definition.get("mode") not in ("generated", "static"):
        raise ValueError(f"{path}: mode must be generated or static")
    validate_expected(definition.get("expected"), definition.get("reasoning_fields"))
    definition["comparison"] = comparison_options(definition.get("comparison"))
    for key in ("task_id", "description"):
        if key in definition and (not isinstance(definition[key], str) or not definition[key].strip()):
            raise ValueError(f"{path}: {key} must be a nonempty string")
    return definition


def resolve_expected(value, references):
    if isinstance(value, dict):
        if "$ref" in value:
            field = value["$ref"]
            if set(value) != {"$ref"} or not isinstance(field, str) or field not in references:
                raise ValueError(f"Unknown or invalid generated reference: {field!r}")
            return references[field]
        return {key: resolve_expected(item, references) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_expected(item, references) for item in value]
    return value


def build_task(name, extra_records=0):
    definition = load_expectation(name)
    generated = definition["mode"] == "generated"
    data = GENERATED_TASKS[name](extra_records) if generated else {
        "reference_values": {}, "template_values": {}, "record_count": 0, "task_data": {}}
    expected = resolve_expected(definition["expected"], data["reference_values"])
    reasoning = validate_expected(expected, definition.get("reasoning_fields"))
    example = definition.get("output_example")
    if generated and example is None and "output_example" in template_fields(Template(read_prompt(name))):
        raise ValueError(f"{name}.json: output_example is required by the Markdown template")
    if example is not None:
        validate_expected(example)
        if example.keys() != expected.keys() or any(type(example[key]) is not type(expected[key]) for key in expected):
            raise ValueError(f"{name}.json: output_example must match the expected keys and value types")
    prompt = (render_prompt(name, **data["template_values"], output_example=json.dumps(example, ensure_ascii=False))
              if generated else read_prompt(name))
    return {"task_id": definition.get("task_id", name),
            "task_description": definition.get("description", f"Custom {name} prompt."),
            "task_mode": definition["mode"], "prompt": prompt, "record_count": data["record_count"],
            "task_data": data["task_data"], "expected": expected, "reasoning_fields": reasoning,
            "output_example": example, "comparison": definition["comparison"]}


def read_prompt(name):
    path = PROMPT_DIR / (name + ".md")
    text = path.read_text(encoding="utf-8").rstrip("\r\n")
    if not text.strip():
        raise ValueError(f"Prompt template is empty: {path}")
    return text


def template_fields(template):
    return {match.group("named") or match.group("braced")
            for match in template.pattern.finditer(template.template)}


def render_prompt(name, **values):
    """Fill Markdown templates without interpreting their literal JSON braces."""
    template = Template(read_prompt(name))
    record_field = {"short": "receipts", "normal": "quotes", "long": "events"}[name]
    fields = template_fields(template)
    if record_field not in fields:
        raise ValueError(f"{name}.md must include ${record_field} so context fitting can add records")
    try:
        return template.substitute(values)
    except (KeyError, ValueError) as error:
        raise ValueError(f"Invalid placeholder in {name}.md: {error}") from error


SYSTEM = read_prompt("system")


def short_data(extra_records=0):
    receipts = [{"id": "R01", "units": 17}, {"id": "R02", "units": 25}]
    receipts += [{"id": f"R{i + 3:02d}", "units": 2 + (i * 3) % 7} for i in range(extra_records)]
    item, reserved, requested = "MONITOR", 9, 40
    available = sum(row["units"] for row in receipts) - reserved
    return {"record_count": len(receipts),
            "template_values": {"item": item, "reserved": reserved, "requested": requested,
                "receipts": "\n".join(f"Receipt {row['id']}: {row['units']} units." for row in receipts)},
            "task_data": {"item": item, "receipts": receipts, "reserved": reserved, "requested": requested},
            "reference_values": {"item": item, "available_units": available, "fulfillable": available >= requested}}


def medium_data(extra_records=0):
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
    return {"record_count": len(vendors),
            "template_values": {"order_units": units, "deadline_days": deadline, "quotes": quotes},
            "task_data": {"quotes": vendors, "order_units": units, "deadline_days": deadline},
            "reference_values": {"vendor": winner["vendor"], "landed_cost": cost(winner),
                                 "eligible_vendors": len(eligible), "delivery_days": winner["days"]}}


def long_data(extra_records=0):
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
    return {"record_count": len(events),
            "template_values": {"events": event_lines, "corrections": "\n".join(corrections), "final_site": "SBY",
                                "opening_units": opening, "demand_units": demand, "reserved_units": reserved},
            "task_data": {"sites": sites, "events": events, "corrections": patches, "final_site": "SBY",
                          "opening_units": opening, "reserved_units": reserved, "demand_units": demand},
            "reference_values": {"destination": sites["SBY"], "available_units": available,
                                 "shortfall_units": shortfall, "action": "REORDER" if shortfall else "RELEASE"}}


GENERATED_TASKS = {"short": short_data, "normal": medium_data, "long": long_data}


def short_task(extra_records=0):
    return build_task("short", extra_records)


def medium_task(extra_records=0):
    return build_task("normal", extra_records)


def long_task(extra_records=0):
    return build_task("long", extra_records)


TASK_BUILDERS = {"Short": short_task, "Medium": medium_task, "Long": long_task}
