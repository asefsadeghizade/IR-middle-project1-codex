from __future__ import annotations

from models.schemas import (
    AST,
    Behavior,
    CrudBehavior,
    GenericAst,
    IfAst,
    NavigationBehavior,
    StateUpdateBehavior,
    UnknownBehavior,
    ValidationBehavior,
)


def classify(ast: AST) -> Behavior:
    """Rule-based behavior classification for parsed trigger ASTs."""
    if isinstance(ast, IfAst):
        for action in ast.actions:
            if action.type == "message":
                return ValidationBehavior(
                    type="validation",
                    field=ast.condition.left,
                    rule=f"{ast.condition.left} {ast.condition.operator} {ast.condition.right}",
                    message=action.value,
                )
        return UnknownBehavior(type="unknown", reason="IF without supported validation action")

    if ast.type == "assignment":
        return StateUpdateBehavior(type="state_update", target=ast.target, value=ast.value)

    if isinstance(ast, GenericAst):
        if ast.statement == "INSERT":
            return CrudBehavior(type="crud", operation="insert")
        if ast.statement.startswith("GO_ITEM"):
            target = ast.statement.split(":", maxsplit=1)[1] if ":" in ast.statement else None
            return NavigationBehavior(type="navigation", target=target)

    return UnknownBehavior(type="unknown", reason=f"No rule for AST type {ast.type}")
