from __future__ import annotations

import re

from models.schemas import (
    AST,
    AssignmentAction,
    AssignmentAst,
    Condition,
    GenericAst,
    IfAst,
    MessageAction,
)


_IF_RE = re.compile(
    r"^IF\s+:(?P<left>[A-Za-z_][\w$#]*)\s*(?P<op>>|=)\s*(?P<right>\d+)\s+THEN\s*(?P<body>.+?)\s*END\s+IF\s*;?$",
    re.IGNORECASE | re.DOTALL,
)
_ASSIGN_RE = re.compile(
    r"^:(?P<target>[A-Za-z_][\w$#]*)\s*:=\s*(?P<value>\d+)\s*;?$",
    re.IGNORECASE,
)
_MESSAGE_RE = re.compile(r"^MESSAGE\('(?P<value>[^']*)'\)\s*;?$", re.IGNORECASE)


class ParseError(ValueError):
    """Raised when the simplified parser cannot parse supported syntax."""


def parse_trigger_code(code: str) -> AST:
    """Parse supported Oracle Forms trigger snippets into a simplified AST."""
    normalized = code.strip()

    if if_match := _IF_RE.match(normalized):
        condition = Condition(
            left=if_match.group("left").upper(),
            operator=if_match.group("op"),
            right=int(if_match.group("right")),
        )
        actions = _parse_actions(if_match.group("body"))
        return IfAst(type="if", condition=condition, actions=actions)

    if assignment := _ASSIGN_RE.match(normalized):
        return AssignmentAst(
            type="assignment",
            target=assignment.group("target").upper(),
            value=int(assignment.group("value")),
        )

    upper_stmt = normalized.upper()
    if upper_stmt.startswith("INSERT"):
        return GenericAst(type="statement", statement="INSERT")
    if upper_stmt.startswith("GO_ITEM"):
        target_match = re.search(r"GO_ITEM\('\s*([^']+?)\s*'\)", normalized, re.IGNORECASE)
        target = target_match.group(1).upper() if target_match else "GO_ITEM"
        return GenericAst(type="statement", statement=f"GO_ITEM:{target}")

    raise ParseError(f"Unsupported syntax: {code}")


def _parse_actions(body: str) -> list[MessageAction | AssignmentAction]:
    raw_actions = [part.strip() for part in body.split(";") if part.strip()]
    parsed_actions: list[MessageAction | AssignmentAction] = []

    for action in raw_actions:
        if message := _MESSAGE_RE.match(action):
            parsed_actions.append(MessageAction(type="message", value=message.group("value")))
            continue
        if assignment := _ASSIGN_RE.match(action):
            parsed_actions.append(
                AssignmentAction(
                    type="assignment",
                    target=assignment.group("target").upper(),
                    value=int(assignment.group("value")),
                )
            )
            continue
        raise ParseError(f"Unsupported action inside IF: {action}")

    return parsed_actions
