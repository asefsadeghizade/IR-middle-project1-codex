from __future__ import annotations

from models.schemas import (
    Behavior,
    CrudBehavior,
    FrontendValidationMap,
    MappedOutput,
    NavigationBehavior,
    StateUpdateBehavior,
    StateUpdateMap,
    UnknownMap,
    ValidationBehavior,
    CrudMap,
    NavigationMap,
)


def map_behavior(behavior: Behavior) -> MappedOutput:
    """Map semantic behavior to modern JavaScript constructs."""
    if isinstance(behavior, ValidationBehavior):
        field = behavior.field.lower()
        function_name = f"validate_{field}"
        code = (
            f"function {function_name}({field}) {{ "
            f"if ({field} {behavior.rule.split(' ', 1)[1].replace(behavior.field, field)}) return '{behavior.message}'; "
            "return null; }"
        )
        return FrontendValidationMap(type="frontend_validation", function=function_name, code=code)

    if isinstance(behavior, StateUpdateBehavior):
        target = behavior.target[0] + behavior.target[1:].lower()
        return StateUpdateMap(type="state_update", code=f"set{target}({behavior.value});")

    if isinstance(behavior, CrudBehavior):
        return CrudMap(type="crud_handler", code="await api.createRecord(payload);")

    if isinstance(behavior, NavigationBehavior):
        target = behavior.target.lower() if behavior.target else "nextField"
        return NavigationMap(type="navigation", code=f"focusField('{target}');")

    return UnknownMap(type="unknown", code="// no mapping available")
