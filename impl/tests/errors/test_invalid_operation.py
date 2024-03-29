import pytest
from _pytest.capture import CaptureFixture

from compiler.compiler import run
from compiler.env import RuntimeEnvironment, TypeEnvironment
from compiler.errors import InvalidOperationError, OperandSpan
from compiler.parser import parse, parse_tree_to_ast

EMPTY_ENV = RuntimeEnvironment()
EMPTY_TYPE_ENV = TypeEnvironment()


def test_unary_op_bool_error():
    with pytest.raises(InvalidOperationError) as excinfo:
        ast = parse_tree_to_ast(parse("-true"))
        ast.typecheck(EMPTY_TYPE_ENV)

    err = excinfo.value

    assert err.span.coord() == ((1, 1), (1, 6))
    assert err.operator.name == "-"
    assert err.operator.span.coord() == ((1, 1), (1, 2))

    match err.operands:
        case [OperandSpan(type_=type_, span=span)]:
            assert type_.name == "Bool"
            assert span.coord() == ((1, 2), (1, 6))
        case _:
            assert False


def test_unary_op_bool_error_output(capfd: CaptureFixture[str], snapshot: str):
    run("-true", EMPTY_TYPE_ENV, EMPTY_ENV)
    _, err = capfd.readouterr()
    assert snapshot == err


def test_binary_op_bool_error():
    with pytest.raises(InvalidOperationError) as excinfo:
        ast = parse_tree_to_ast(parse("true+false"))
        #                              123456789
        ast.typecheck(EMPTY_TYPE_ENV)

    err = excinfo.value

    assert err.span.coord() == ((1, 1), (1, 11))
    assert err.operator.name == "+"
    assert err.operator.span.coord() == ((1, 5), (1, 6))

    match err.operands:
        case [OperandSpan(type_=t1, span=s1), OperandSpan(type_=t2, span=s2)]:
            assert t1.name == "Bool"
            assert s1.coord() == ((1, 1), (1, 5))
            assert t2.name == "Bool"
            assert s2.coord() == ((1, 6), (1, 11))
        case _:
            assert False


def test_binary_op_bool_error_output(capfd: CaptureFixture[str], snapshot: str):
    run("true+false", EMPTY_TYPE_ENV, EMPTY_ENV)
    _, err = capfd.readouterr()
    assert snapshot == err


def test_binary_op_bool_int_error():
    with pytest.raises(InvalidOperationError) as excinfo:
        ast = parse_tree_to_ast(parse("24+false"))
        #                              123456789
        ast.typecheck(EMPTY_TYPE_ENV)

    err = excinfo.value

    assert err.span.coord() == ((1, 1), (1, 9))
    assert err.operator.name == "+"
    assert err.operator.span.coord() == ((1, 3), (1, 4))

    match err.operands:
        case [OperandSpan(type_=t1, span=s1), OperandSpan(type_=t2, span=s2)]:
            assert t1.name == "Int"
            assert s1.coord() == ((1, 1), (1, 3))
            assert t2.name == "Bool"
            assert s2.coord() == ((1, 4), (1, 9))
        case _:
            assert False


def test_binary_op_bool_int_error_output(capfd: CaptureFixture[str], snapshot: str):
    run("24+false", EMPTY_TYPE_ENV, EMPTY_ENV)
    _, err = capfd.readouterr()
    assert snapshot == err
