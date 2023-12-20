from typing import Literal, Union
import dataclasses
from dataclasses import dataclass

from lark import ast_utils

from . import langtypes

_LispAst = list[Union[str, "_LispAst"]]


# TODO: explain requirement of underscore by lark
@dataclass
class _Ast(ast_utils.Ast):
    def __init__(self):
        self._type: langtypes.Type | None = None

    def to_untyped_sexp(self) -> _LispAst:
        classname = type(self).__name__

        lisp_ast: _LispAst = [classname]

        for field in dataclasses.fields(self):
            lisp_ast.append(":")
            lisp_ast.append(field.name)

            value = getattr(self, field.name)
            if isinstance(value, _Ast):
                lisp_ast.append(value.to_untyped_sexp())
            else:
                lisp_ast.append(str(value))

        return lisp_ast

    def to_typed_sexp(self) -> _LispAst:
        classname = type(self).__name__
        type_ = type(self._type).__name__

        lisp_ast: _LispAst = [classname, type_]

        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if isinstance(value, _Ast):
                lisp_ast.append(":")
                lisp_ast.append(field.name)
                lisp_ast.append(value.to_typed_sexp())

        return lisp_ast


class _Expression(_Ast):
    pass


@dataclass
class UnaryOp(_Expression):
    op: Literal["+", "-"]
    operand: _Expression


@dataclass
class BoolLiteral(_Expression):
    value: bool


@dataclass
class IntLiteral(_Expression):
    value: bool
