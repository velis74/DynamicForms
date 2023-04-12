from __future__ import annotations

from collections import namedtuple
from enum import IntEnum
from typing import Tuple, Union, Iterable, NamedTuple


class ConditionalVisibilityMixin(object):
    def __init__(self, *args, conditional_visibility: Statement = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.conditional_visibility = conditional_visibility

    def as_component_def(self) -> dict:
        try:
            res = super().as_component_def()  # noqa
        except AttributeError:
            res = dict()
        res.update(dict(conditional_visibility=self.conditional_visibility.to_value()))
        return res


class Operators(IntEnum):
    # Logic Operators
    NOT = 0
    OR = 1
    AND = 2
    XOR = 3
    NAND = 4
    NOR = 5

    # Comparators
    EQUALS = -1
    NOT_EQUALS = -2
    GT = -3
    LT = -4
    GE = -5
    LE = -6
    INCLUDED = -7


LogicOperators = [
    Operators.OR,
    Operators.AND,
    Operators.XOR,
    Operators.NAND,
    Operators.NOR,
]

Comparators = [
    Operators.EQUALS,
    Operators.NOT_EQUALS,
    Operators.GT,
    Operators.LT,
    Operators.GE,
    Operators.LE,
    Operators.INCLUDED,
]


# Types
FieldType = str


class ExpressionType(NamedTuple):
    field_name: str
    operator: Operators
    value: any


class StatementType(NamedTuple):
    statement_a: Union[FieldType, ExpressionType]
    operator: Operators
    statement_b: Union[any, ExpressionType]


class Field(object):
    """
    Abstraction of field name. Object is used to make statements inline with comparison operators such as
    equals,

    Arguments:
    :field_name: Name of a field to use comparison function on
    """

    def __init__(self, field_name: str):
        self.field_name = field_name

    def to_value(self) -> FieldType:
        return self.field_name

    def __eq__(self, other: any) -> Statement:
        return Statement(self.field_name, Operators.EQUALS, other)

    def __gt__(self, other: any) -> Statement:
        return Statement(self.field_name, Operators.GT, other)

    def __ge__(self, other: any) -> Statement:
        return Statement(self.field_name, Operators.GE, other)

    def __le__(self, other: any) -> Statement:
        return Statement(self.field_name, Operators.LE, other)

    def __lt__(self, other: any) -> Statement:
        return Statement(self.field_name, Operators.LT, other)

    def __ne__(self, other: any) -> Statement:
        return Statement(self.field_name, Operators.NOT_EQUALS, other)

    def included(self, other: Iterable) -> Statement:
        return Statement(self.field_name, Operators.INCLUDED, other)


class Statement:
    """
    Statement represents a single statement in boolean algebra. Since boolean algebra statements are recursive,
    one statement can be composed of multiple statements, statement can be of 2 different types. One is a comparison
    on field value and the other is a composition of comparisons.

    Names of init params can be decieving so please read the following documentation

    Arguments:
    :statement_a: Is either a nested statement [Statement] or a name of the field [str]
    :operator: Type of common boolean algebra operators [LogicOperators] or comparison operator [Comparator]
    :statement_b: Is either a nested statement [Statement] or a value to compare a field with [any]
    """

    def __init__(
        self,
        statement_a: Union[str, Statement],
        operator: Operators,
        statement_b: Union[any, Statement],
    ):
        self.statement_a = statement_a
        self.operator = operator
        self.statement_b = statement_b

        self.validation()

    def validation(self) -> None:
        if self.operator == Operators.INCLUDED:
            try:
                len(self.statement_b)
            except TypeError:
                raise ValueError(f"Operator INCLUDED expects an iterable value, got {self.statement_b}")
        if self.operator in LogicOperators:
            if not (isinstance(self.statement_a, S) and isinstance(self.statement_b, S)):
                raise ValueError(
                    f"Logic operators expect a Statement type variables,"
                    f"got {type(self.statement_a)}, {type(self.statement_b)}"
                )
        else:
            # We are using comparator
            if isinstance(self.statement_a, S) and isinstance(self.statement_b, S):
                raise ValueError(f"Comparators expect non Statement type variables")
            if not isinstance(self.statement_a, str):
                raise ValueError(f"Comparators expects first value to be string type, got {type(self.statement_a)}")

    def __or__(self, other: Statement) -> Statement:
        return Statement(self, Operators.OR, other)

    def __and__(self, other: Statement):
        return Statement(self, Operators.AND, other)

    def __xor__(self, other: Statement):
        return Statement(self, Operators.XOR, other)

    def to_value(self) -> StatementType:
        if isinstance(self.statement_a, Statement) and isinstance(self.statement_b, Statement):
            return self.statement_a.to_value(), self.operator, self.statement_b.to_value()
        return self.statement_a, self.operator, self.statement_b


# Aliases for developer friendly experience
F = Field
S = Statement
