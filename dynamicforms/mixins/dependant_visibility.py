from __future__ import annotations

from enum import IntEnum
from typing import Tuple, Union


class DependantVisibilityMixin(object):
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


class LogicOperators(IntEnum):
    NOT = 0
    OR = 1
    AND = 2
    XOR = 3
    NAND = 4
    NOR = 5


class Comparators(IntEnum):
    EQUALS = 0
    NOT_EQUALS = 1
    GT = 2
    LT = 3
    GE = 4
    LE = 5


# Types
Operators = Union[LogicOperators, Comparators]
FieldType = str
ExpressionType = Tuple[str, Operators, any]
StatementType = Tuple[Union[FieldType, ExpressionType], Operators, Union[any, ExpressionType]]


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
        return Statement(self.field_name, Comparators.EQUALS, other)

    def __gt__(self, other: any) -> Statement:
        return Statement(self.field_name, Comparators.GT, other)

    def __ge__(self, other: any) -> Statement:
        return Statement(self.field_name, Comparators.GE, other)

    def __le__(self, other: any) -> Statement:
        return Statement(self.field_name, Comparators.LE, other)

    def __lt__(self, other: any) -> Statement:
        return Statement(self.field_name, Comparators.LT, other)

    def __ne__(self, other: any) -> Statement:
        return Statement(self.field_name, Comparators.NOT_EQUALS, other)


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

    def __or__(self, other: Statement) -> Statement:
        return Statement(self, LogicOperators.OR, other)

    def __and__(self, other: Statement):
        return Statement(self, LogicOperators.AND, other)

    def __xor__(self, other: Statement):
        return Statement(self, LogicOperators.XOR, other)

    def to_value(self) -> StatementType:
        """
        :returns:
        """
        if isinstance(self.statement_a, Statement) and isinstance(self.statement_b, Statement):
            return self.statement_a.to_value(), self.operator, self.statement_b.to_value()
        return self.statement_a, self.operator, self.statement_b


# Aliases for developer friendly experience (or probably in some cases, another case of WTFs)
F = Field
S = Statement
