import pytest

from models.schemas import AssignmentAst, IfAst
from parser.plsql_parser import ParseError, parse_trigger_code


def test_parse_simple_if_message():
    ast = parse_trigger_code("IF :SAL > 5000 THEN MESSAGE('Too high'); END IF;")
    assert isinstance(ast, IfAst)
    assert ast.condition.left == "SAL"
    assert ast.condition.operator == ">"
    assert ast.actions[0].type == "message"
    assert ast.actions[0].value == "Too high"


def test_parse_assignment():
    ast = parse_trigger_code(":A := 5;")
    assert isinstance(ast, AssignmentAst)
    assert ast.target == "A"
    assert ast.value == 5


def test_parse_equality_condition():
    ast = parse_trigger_code("IF :SAL = 0 THEN MESSAGE('Required'); END IF;")
    assert isinstance(ast, IfAst)
    assert ast.condition.operator == "="
    assert ast.condition.right == 0


def test_parse_invalid_syntax_raises_error():
    with pytest.raises(ParseError):
        parse_trigger_code("WHILE :SAL > 0 LOOP MESSAGE('bad'); END LOOP;")


def test_parse_if_multiple_actions():
    ast = parse_trigger_code("IF :SAL > 7000 THEN MESSAGE('Warn'); :GRADE := 5; END IF;")
    assert isinstance(ast, IfAst)
    assert len(ast.actions) == 2
    assert ast.actions[0].type == "message"
    assert ast.actions[1].type == "assignment"
