import pytest
from _pytest.capture import CaptureFixture

from compiler.compiler import run
from compiler.env import RuntimeEnvironment, TypeEnvironment
from compiler.errors import ArrayTypeMismatch
from compiler.langtypes import BOOL, INT
from compiler.parser import parse, parse_tree_to_ast

EMPTY_ENV = RuntimeEnvironment()
EMPTY_TYPE_ENV = TypeEnvironment()


def test_array_elements_type_mismatch():
    with pytest.raises(ArrayTypeMismatch) as excinfo:
        ast = parse_tree_to_ast(parse("let x = [1, true]"))
        ast.typecheck(EMPTY_TYPE_ENV)

    err = excinfo.value

    assert err.span.coord() == ((1, 13), (1, 17))
    assert err.expected_type_span.coord() == ((1, 10), (1, 11))
    assert err.expected_type == INT
    assert err.actual_type == BOOL


def test_array_elements_type_mismatch_output(capfd: CaptureFixture[str], snapshot: str):
    run("let x = [1, true]", EMPTY_TYPE_ENV, EMPTY_ENV)
    _, err = capfd.readouterr()
    assert snapshot == err
