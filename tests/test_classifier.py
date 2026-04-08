from classifier.behavior_classifier import classify
from models.schemas import AssignmentAst, Condition, GenericAst, IfAst, MessageAction


def test_validation_detection():
    ast = IfAst(
        type="if",
        condition=Condition(left="SAL", operator=">", right=5000),
        actions=[MessageAction(type="message", value="Too high")],
    )
    behavior = classify(ast)
    assert behavior.type == "validation"
    assert behavior.field == "SAL"


def test_assignment_detection():
    behavior = classify(AssignmentAst(type="assignment", target="A", value=5))
    assert behavior.type == "state_update"
    assert behavior.target == "A"


def test_unknown_pattern_fallback():
    behavior = classify(GenericAst(type="statement", statement="UNSUPPORTED"))
    assert behavior.type == "unknown"
