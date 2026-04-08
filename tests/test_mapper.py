from mapper.pattern_mapper import map_behavior
from models.schemas import StateUpdateBehavior, ValidationBehavior


def test_validation_mapping():
    behavior = ValidationBehavior(
        type="validation",
        field="SAL",
        rule="SAL > 5000",
        message="Too high",
    )
    mapped = map_behavior(behavior)
    assert mapped.type == "frontend_validation"
    assert "validate_sal" in mapped.function
    assert "Too high" in mapped.code


def test_assignment_mapping():
    behavior = StateUpdateBehavior(type="state_update", target="A", value=5)
    mapped = map_behavior(behavior)
    assert mapped.type == "state_update"
    assert mapped.code == "setA(5);"
