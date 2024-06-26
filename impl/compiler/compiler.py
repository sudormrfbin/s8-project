from typing import Any

from compiler.env import RuntimeEnvironment, TypeEnvironment

from compiler import builtins, errors, langtypes, langvalues
from compiler.parser import parse, parse_tree_to_ast

BUILTIN_FUNCTIONS: list[type[langvalues.BuiltinFunction]] = [
    builtins.SumFunction,
    builtins.ArrayLengthFunction,
    builtins.StringLengthFunction,
    builtins.ArrayAppend,
]

BUILTIN_TYPES: list[langtypes.Primitive] = [
    langtypes.INT,
    langtypes.BOOL,
    langtypes.STRING,
]


def get_default_environs() -> tuple[TypeEnvironment, RuntimeEnvironment]:
    type_env = TypeEnvironment()
    runtime_env = RuntimeEnvironment()

    for fn in BUILTIN_FUNCTIONS:
        type_env.define_var_type(fn.TYPE.function_name, fn.TYPE)
        runtime_env.define(fn.TYPE.function_name, fn())

    for ty in BUILTIN_TYPES:
        type_env.define_type(langtypes.name(ty), ty)

    return (type_env, runtime_env)


def run(source: str, type_env: TypeEnvironment, runtime_env: RuntimeEnvironment) -> Any:
    try:
        return _run(source, type_env, runtime_env)
    except errors.CompilerError as err:
        err.report(source)


def _run(
    source: str, type_env: TypeEnvironment, runtime_env: RuntimeEnvironment
) -> Any:
    tree = parse(source)
    ast = parse_tree_to_ast(tree)

    ast.typecheck(type_env)

    return ast.eval(runtime_env)
