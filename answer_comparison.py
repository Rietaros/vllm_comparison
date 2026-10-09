"""JSON answer comparison configured by each prompt's expectation file."""
from __future__ import annotations

import json
import math
import re

SCORING_POLICY = "configured-json-fields-v1"
DEFAULT_COMPARISON = {"allow_extra_fields": False, "case_sensitive": True}


def comparison_options(options=None):
    options = {} if options is None else options
    if not isinstance(options, dict) or set(options) - set(DEFAULT_COMPARISON):
        raise ValueError("comparison supports only allow_extra_fields and case_sensitive")
    if any(type(value) is not bool for value in options.values()):
        raise ValueError("comparison options must be true or false")
    return {**DEFAULT_COMPARISON, **options}


def validate_expected(expected, reasoning_fields=None):
    if not isinstance(expected, dict) or not expected or any(not isinstance(key, str) or not key for key in expected):
        raise ValueError("expected must be a nonempty JSON object with nonempty field names")
    # JSON's NaN/Infinity extensions cannot be valid reference answers.
    try:
        json.dumps(expected, allow_nan=False)
    except (ValueError, TypeError) as error:
        raise ValueError("expected must contain finite JSON values") from error
    fields = list(expected) if reasoning_fields is None else reasoning_fields
    if (not isinstance(fields, list) or any(not isinstance(key, str) or key not in expected for key in fields)
            or len(set(fields)) != len(fields)):
        raise ValueError("reasoning_fields must list unique fields from expected")
    return fields


def reject_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def score_answer(text, expected, reasoning_fields=None, comparison=None):
    """Keep strict JSON types; optionally allow extra keys or ignore string case."""
    fields = validate_expected(expected, reasoning_fields)
    options = comparison_options(comparison)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE).strip()
    try:
        parsed = json.loads(cleaned, parse_constant=reject_constant)
        json.dumps(parsed, allow_nan=False)
    except (ValueError, TypeError):
        parsed = None

    def exact(value, reference):
        if type(value) is not type(reference):
            return False
        if isinstance(reference, list):
            return len(value) == len(reference) and all(exact(v, r) for v, r in zip(value, reference))
        if isinstance(reference, dict):
            keys_valid = (reference.keys() <= value.keys() if options["allow_extra_fields"]
                          else value.keys() == reference.keys())
            return keys_valid and all(exact(value[key], item) for key, item in reference.items())
        if isinstance(reference, str) and not options["case_sensitive"]:
            return value.casefold() == reference.casefold()
        if isinstance(reference, float) and not math.isfinite(value):
            return False
        return value == reference

    # Missing null-valued fields must still fail; absence is not JSON null.
    correct = {key: isinstance(parsed, dict) and key in parsed and exact(parsed[key], reference)
               for key, reference in expected.items()}
    schema_valid = isinstance(parsed, dict) and (expected.keys() <= parsed.keys() if options["allow_extra_fields"]
                                                else parsed.keys() == expected.keys())
    return {"parsed_answer": parsed, "json_valid": isinstance(parsed, dict), "schema_valid": schema_valid,
            "field_accuracy": sum(correct.values()) / len(expected),
            "reasoning_accuracy": sum(correct[key] for key in fields) / len(fields) if fields else None,
            "all_fields_correct": schema_valid and all(correct.values()), "field_correct": correct}
