from __future__ import annotations

from classifier.behavior_classifier import classify
from mapper.pattern_mapper import map_behavior
from parser.plsql_parser import parse_trigger_code


def run_pipeline(ir_input: dict) -> list[dict]:
    """Run parse -> classify -> map for each trigger in IR input."""
    results: list[dict] = []

    for trigger in ir_input.get("triggers", []):
        code = trigger.get("code", "")
        ast = parse_trigger_code(code)
        behavior = classify(ast)
        mapped = map_behavior(behavior)

        results.append(
            {
                "trigger": trigger.get("type", "UNKNOWN"),
                "behavior": behavior.type,
                "mapped_code": mapped.code,
                "ast": ast,
                "behavior_detail": behavior,
                "mapping_detail": mapped,
            }
        )

    return results
