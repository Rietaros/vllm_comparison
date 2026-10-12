"""Independent reference checks against the authored passages, not the JSON files."""
import re
from datetime import datetime, timedelta


def math_answer(case_id, text):
    def number(pattern):
        return int(re.search(pattern, text).group(1))

    def numbers(pattern):
        return tuple(map(int, re.search(pattern, text).groups()))

    if case_id == "short-01":
        opening = number(r"Opening usable stock: (\d+)")
        receipts = sum(numbers(r"Accepted receipts: (\d+) units and (\d+) units"))
        available = opening + receipts - number(r"Existing reservations: (\d+)")
        return {"item": re.search(r"Inventory decision for (\w+)", text).group(1),
                "available_units": available, "fulfillable": available >= number(r"New customer request: (\d+)")}
    if case_id == "short-02":
        price_s, price_d = numbers(r"sandwiches for (\d+) credits each and drinks for (\d+) credits")
        count_s, count_d = numbers(r"buys (\d+) sandwiches and (\d+) drinks")
        subtotal = price_s * count_s + price_d * count_d
        return {"subtotal": subtotal, "total": subtotal - number(r"voucher worth (\d+)")}
    if case_id == "short-03":
        distance, speed = numbers(r"travels (\d+) km at a constant (\d+) km")
        minutes = distance * 60 // speed
        departure = datetime.strptime(re.search(r"departs at (\d+:\d+)", text).group(1), "%H:%M")
        return {"travel_minutes": minutes, "arrival": (departure + timedelta(minutes=minutes)).strftime("%H:%M")}
    if case_id == "short-04":
        length, width = numbers(r"is (\d+) meters long and (\d+) meters wide")
        pond_length, pond_width = numbers(r"pond inside it is (\d+) meters by (\d+) meters")
        return {"garden_area": length * width, "planted_area": length * width - pond_length * pond_width}
    if case_id == "short-05":
        correct, incorrect = numbers(r"has (\d+) correct, (\d+) incorrect")
        score = correct * number(r"awards (\d+) points") - incorrect * number(r"subtracts (\d+) point")
        return {"score": score, "passed": score >= number(r"at least (\d+) points")}
    if case_id == "medium-01":
        plant, standard = numbers(r"guests: (\d+) need plant meals and the other (\d+) need standard")
        plant_price, standard_price = numbers(r"charges (\d+) credits per plant meal and (\d+) credits per standard")
        cost = plant * plant_price + standard * standard_price + number(r"service fee of (\d+)") - number(r"voucher of (\d+)")
        budget = number(r"budget is (\d+)")
        return {"total_cost": cost, "budget_remaining": budget - cost, "within_budget": cost <= budget}
    if case_id == "medium-02":
        consumption = number(r"Closing meter: (\d+)") - number(r"Opening meter: (\d+)")
        chargeable = max(0, consumption - number(r"first (\d+) cubic meters"))
        invoice = chargeable * number(r"allowance costs (\d+) credits") + number(r"fixed charge is (\d+)")
        return {"consumption": consumption, "chargeable_volume": chargeable, "invoice": invoice}
    if case_id == "medium-03":
        rate = number(r"costing (\d+) credits per kilometer")
        deadline = number(r"at most (\d+) minutes")
        eligible = [(int(distance) * rate + int(toll), int(time), name)
                    for name, distance, toll, time, state in re.findall(
                        r"(\w+): distance (\d+) km; toll (\d+) credits; travel time (\d+) minutes; road (open|closed)", text)
                    if state == "open" and int(time) <= deadline]
        cost, _, route = min(eligible)
        return {"route": route, "total_cost": cost, "eligible_routes": len(eligible)}
    if case_id == "medium-04":
        batches = [(int(made), int(rejected)) for made, rejected, status in re.findall(
            r"Batch \w+: manufactured (\d+); rejected (\d+); status (\w+)", text) if status == "released"]
        usable = sum(made - rejected for made, rejected in batches)
        return {"usable_units": usable, "rejected_units": sum(rejected for _, rejected in batches),
                "shortfall": max(0, number(r"needs (\d+) usable sensors") - usable)}
    if case_id == "medium-05":
        chapters, duration = numbers(r"study (\d+) chapters\. Each chapter requires (\d+) minutes")
        planned = (2 * number(r"Tuesday: two sessions of (\d+) minutes")
                   + number(r"Wednesday: one session of (\d+) minutes")
                   + number(r"Thursday: one session of (\d+) minutes"))
        return {"planned_minutes": planned, "additional_minutes": max(0, chapters * duration - planned),
                "completed_chapters": min(chapters, planned // duration)}
    if case_id == "long-01":
        rows = {eid: [direction, int(amount), status, restriction] for eid, direction, amount, status, restriction
                in re.findall(r"(E\d+) \| (IN|OUT) \| amount (\d+) \| status (\w+)(?: \| restriction (\w+))?", text)}
        for eid, amount in re.findall(r"replace (?:expense )?(E\d+)'s amount with (\d+)", text):
            rows[eid][1] = int(amount)
        balance = number(r"begins with (\d+) unrestricted credits")
        for direction, amount, status, restriction in rows.values():
            if direction == "IN" and status == "posted" and restriction == "unrestricted":
                balance += amount
            elif direction == "OUT" and status == "paid":
                balance -= amount
        spendable = balance - number(r"reserve (\d+) credits")
        return {"unrestricted_balance": balance, "spendable_balance": spendable,
                "shortfall": max(0, number(r"workshop needs (\d+) credits") - spendable)}
    if case_id == "long-02":
        rows = {eid: [int(energy), tariff, direction, status] for eid, energy, tariff, direction, status in re.findall(
            r"([A-P]) \| energy (\d+) \| tariff (\w+) \| direction (\w+) \| status (\w+)", text)}
        for eid, energy in re.findall(r"replaces ([A-P])'s energy with (\d+) kWh", text):
            rows[eid][0] = int(energy)
        for eid, status in re.findall(r"replaces ([A-P])'s status with (\w+)", text):
            rows[eid][3] = status
        totals = {tariff: sum(energy for energy, label, direction, status in rows.values()
                             if label == tariff and direction == "import" and status == "accepted")
                  for tariff in ("peak", "off_peak")}
        invoice = (totals["peak"] * number(r"Peak imports cost (\d+)")
                   + totals["off_peak"] * number(r"Off-peak imports cost (\d+)")
                   + number(r"account charge of (\d+)") - number(r"solar credit of (\d+)"))
        return {"peak_kwh": totals["peak"], "off_peak_kwh": totals["off_peak"], "invoice": invoice}
    if case_id == "long-03":
        scores = {component: int(score) for _, student, component, score, status in re.findall(
            r"(\w+) \| student (\w+) \| component (\w+) \| score (\d+) \| status (\w+)", text)
                  if student == "Nara" and status == "assessed"}
        for score in re.findall(r"replaces (?:Nara's project score in NP|NP's score) with (\d+)", text):
            scores["project"] = int(score)
        scores["final"] = number(r"final score in NF as (\d+)")
        weighted = sum(scores[component] * number(rf"{component} contributes (\d+) percent")
                       for component in scores) // 100
        return {"project_score": scores["project"], "final_score": scores["final"],
                "weighted_result": weighted, "passed": weighted >= number(r"at least (\d+)\.")}
    if case_id == "long-04":
        jobs = {eid: [service, int(size), state] for eid, service, size, state in re.findall(
            r"(J\d+) \| service (\w+) \| size (\d+) \| state (\w+)", text)}
        for eid, size in re.findall(r"replaces (J\d+)'s size with (\d+) MiB", text):
            jobs[eid][1] = int(size)
        for eid, state in re.findall(r"replaces (J\d+)'s state with (\w+)", text):
            jobs[eid][2] = state
        required = number(r"base backup of (\d+) MiB") + sum(size for service, size, state in jobs.values()
                                                              if service == "Atlas" and state == "retained")
        remaining = number(r"capacity (\d+) MiB") - number(r"Reserve (\d+) MiB") - required
        return {"required_mib": required, "remaining_mib": remaining, "fits": remaining >= 0}
    if case_id == "long-05":
        rows = {name: [int(academic), int(service), int(leadership), application, recommendation]
                for name, academic, service, leadership, application, recommendation in re.findall(
                    r"(\w+) \| academic (\d+) \| service (\d+) \| leadership (\d+) \| application (\w+) \| recommendation (\w+)", text)}
        for name, academic in re.findall(r"replaces (\w+)'s academic points with (\d+)", text):
            rows[name][0] = int(academic)
        ranking = sorted((-sum(row[:3]), name) for name, row in rows.items()
                         if row[3:] == ["complete", "approved"])
        budget = number(r"budget is (\d+) credits")
        award = number(r"receives exactly (\d+) credits")
        names = [name for _, name in ranking[:budget // award]]
        return {"awardees": names, "bela_score": sum(rows["Bela"][:3]), "remaining_budget": budget - len(names) * award}
    raise AssertionError(f"Missing independent math oracle for {case_id}")


# Human-reviewed answers to the controlling passages, independent of the bank JSON.
QNA_ANSWERS = {
    "short-06": {"resolution": "replacement", "evidence": "damage_photo"},
    "short-07": {"room": "reference room", "may_borrow": False},
    "short-08": {"location": "shaded corner", "cause": "excess light"},
    "short-09": {"channel": "bookmarked security portal", "share_code": False},
    "short-10": {"gallery": "Maritime Gallery", "collection": "Navigation"},
    "medium-06": {"owner": "Mira", "channel": "incident bridge", "first_action": "Preserve application logs"},
    "medium-07": {"room": "Cedar Room", "team": "Facilities", "confirmation": "written confirmation"},
    "medium-08": {"team": "People Operations", "channel": "secure employee portal", "may_publish": False},
    "medium-09": {"contact": "licensed rescue team", "location": "quiet ventilated box", "feeding_allowed": False},
    "medium-10": {"release_action": "corrected page with a correction notice", "owner": "section editor", "retain_history": True},
    "long-06": {"route": "Route Alder", "gathering_place": "North Court", "assistance_team": "Logistics Desk", "channel": "radio channel"},
    "long-07": {"action": "hold", "review_team": "Application Security", "may_waive": False},
    "long-08": {"maker": "Anika", "workshop": "River Workshop", "owner": "City Archive", "image_use": "educational_only"},
    "long-09": {"action": "reinstate", "owner": "Appeals Desk", "evidence": "signed transcript", "authored_abuse": False},
    "long-10": {"audio_action": "delete", "continue_collection": False, "retained_record": "consent withdrawal record", "owner": "Ethics Coordinator"},
}
