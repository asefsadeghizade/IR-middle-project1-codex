from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Condition:
    """Simplified IF condition model for PL/SQL snippets."""

    left: str
    operator: Literal[">", "="]
    right: int


@dataclass(frozen=True)
class MessageAction:
    type: Literal["message"]
    value: str


@dataclass(frozen=True)
class AssignmentAction:
    type: Literal["assignment"]
    target: str
    value: int


Action = MessageAction | AssignmentAction


@dataclass(frozen=True)
class IfAst:
    type: Literal["if"]
    condition: Condition
    actions: list[Action]


@dataclass(frozen=True)
class AssignmentAst:
    type: Literal["assignment"]
    target: str
    value: int


@dataclass(frozen=True)
class GenericAst:
    """Fallback AST for minimally parsed statements such as INSERT/GO_ITEM."""

    type: Literal["statement"]
    statement: str


AST = IfAst | AssignmentAst | GenericAst


@dataclass(frozen=True)
class ValidationBehavior:
    type: Literal["validation"]
    field: str
    rule: str
    message: str


@dataclass(frozen=True)
class StateUpdateBehavior:
    type: Literal["state_update"]
    target: str
    value: int


@dataclass(frozen=True)
class CrudBehavior:
    type: Literal["crud"]
    operation: str


@dataclass(frozen=True)
class NavigationBehavior:
    type: Literal["navigation"]
    target: str | None = None


@dataclass(frozen=True)
class UnknownBehavior:
    type: Literal["unknown"]
    reason: str


Behavior = (
    ValidationBehavior
    | StateUpdateBehavior
    | CrudBehavior
    | NavigationBehavior
    | UnknownBehavior
)


@dataclass(frozen=True)
class FrontendValidationMap:
    type: Literal["frontend_validation"]
    function: str
    code: str


@dataclass(frozen=True)
class StateUpdateMap:
    type: Literal["state_update"]
    code: str


@dataclass(frozen=True)
class CrudMap:
    type: Literal["crud_handler"]
    code: str


@dataclass(frozen=True)
class NavigationMap:
    type: Literal["navigation"]
    code: str


@dataclass(frozen=True)
class UnknownMap:
    type: Literal["unknown"]
    code: str


MappedOutput = FrontendValidationMap | StateUpdateMap | CrudMap | NavigationMap | UnknownMap
