from typing import Any
from compiler.compiler import get_default_environs
from compiler.langvalues import StructValue
from compiler.parser import parse, parse_tree_to_ast
from compiler.langtypes import INT, STRING, Struct
from tests.utils import docstring_source_with_snapshot


# 1. struct type in typeenv


@docstring_source_with_snapshot
def test_struct_def(source: str, snapshot: Any):
    """
    struct Person {
        name: string
        age: int
    }
    """
    ast = parse_tree_to_ast(parse(source))
    assert ast.to_dict() == snapshot

    type_env, _ = get_default_environs()
    ast.typecheck(type_env)
    assert ast.to_type_dict() == snapshot

    assert type_env.get_type("Person") == Struct(
        struct_name="Person",
        members=Struct.Members({"name": STRING, "age": INT}),
    )


@docstring_source_with_snapshot
def test_struct_init(source: str, snapshot: Any):
    """
    struct Person {
        name: string
        age: int
    }

    let p = Person(name="bob", age=23)
    """
    ast = parse_tree_to_ast(parse(source))
    assert ast.to_dict() == snapshot

    type_env, env = get_default_environs()
    ast.typecheck(type_env)
    assert ast.to_type_dict() == snapshot

    ast.eval(env)
    assert env.get("p") == StructValue(
        name="Person",
        attrs={
            "name": "bob",
            "age": 23,
        },
    )
