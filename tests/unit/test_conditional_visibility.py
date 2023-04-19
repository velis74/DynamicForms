from unittest import TestCase

from dynamicforms.mixins.conditional_visibility import Comparators, F, LogicOperators, Operators, S


def create_operator(statement_a, operator, statement_b):
    """Wrapper for initializing statement so we can catch raised errors"""
    return S(statement_a=statement_a, operator=operator, statement_b=statement_b)


class OperatorsTest(TestCase):
    # Test values are pretty much arbitrary, no true meaning behind them except to simplify test cases
    field_name = "Test"
    comparison_value = 10
    comparison_list = [10] * 3
    S1 = S(field_name, Operators.EQUALS, comparison_value)
    S1_value = S1.to_value()

    def _test_iterable_value(self, operator: Operators):
        # Will fail upon not receiving iterable value
        self.assertRaises(
            ValueError, S, statement_a=self.field_name, operator=operator, statement_b=self.comparison_value
        )
        self.assertRaises(ValueError, S, statement_a=self.field_name, operator=operator, statement_b=self.S1)

        # Should not fail when receiving iterable values
        S(statement_a=self.field_name, operator=operator, statement_b=self.comparison_list)  # list
        S(statement_a=self.field_name, operator=operator, statement_b={10, 11, 12})  # set
        S(statement_a=self.field_name, operator=operator, statement_b=(10, 11, 12))  # tuple
        S(statement_a=self.field_name, operator=operator, statement_b=range(10))  # generator

    def test_operator_validation(self):
        # Logic operators with non Statement arguments
        for operator in LogicOperators:
            self.assertRaises(
                ValueError, S, statement_a=self.field_name, operator=operator, statement_b=self.comparison_value
            )

        # Comparators cannot be initiated with both Statement values
        for operator in Comparators:
            self.assertRaises(ValueError, S, statement_a=self.S1, operator=operator, statement_b=self.S1)

        # Comparators expect string as a first value (field name)
        for operator in Comparators:
            self.assertRaises(ValueError, S, statement_a=self.S1, operator=operator, statement_b=self.comparison_value)
            self.assertRaises(
                ValueError, S, statement_a=self.comparison_value, operator=operator, statement_b=self.comparison_value
            )

        self._test_iterable_value(operator=Operators.IN)
        self._test_iterable_value(operator=Operators.NOT_IN)

        # Not operator should only get 1 statement
        self.assertRaises(ValueError, S, statement_a=self.field_name, operator=Operators.NOT, statement_b=self.S1)
        self.assertRaises(ValueError, S, statement_a=self.S1, operator=Operators.NOT, statement_b=self.S1)
        self.assertRaises(
            ValueError, S, statement_a=self.field_name, operator=Operators.NOT, statement_b=self.comparison_value
        )

    def test_field_operations(self):
        self.assertEqual(
            (F(field_name=self.field_name) == self.comparison_value).to_value(),
            (self.field_name, Operators.EQUALS, self.comparison_value),
        )

        self.assertEqual(
            (F(field_name=self.field_name) != self.comparison_value).to_value(),
            (self.field_name, Operators.NOT_EQUALS, self.comparison_value),
        )

        self.assertEqual(
            (F(field_name=self.field_name) > self.comparison_value).to_value(),
            (self.field_name, Operators.GT, self.comparison_value),
        )

        self.assertEqual(
            (F(field_name=self.field_name) >= self.comparison_value).to_value(),
            (self.field_name, Operators.GE, self.comparison_value),
        )

        self.assertEqual(
            (F(field_name=self.field_name) < self.comparison_value).to_value(),
            (self.field_name, Operators.LT, self.comparison_value),
        )

        self.assertEqual(
            (F(field_name=self.field_name) <= self.comparison_value).to_value(),
            (self.field_name, Operators.LE, self.comparison_value),
        )

        self.assertEqual(
            (F(field_name=self.field_name).is_in(self.comparison_list)).to_value(),
            (self.field_name, Operators.IN, self.comparison_list),
        )

    def test_statements_operators(self):
        # Keywords such as and/or cannot be overloaded -> we can simulate this behaviour with bitwise operators
        # the same solution was used in pythons Q objects for database querying
        self.assertEqual((self.S1 & self.S1).to_value(), (self.S1_value, Operators.AND, self.S1_value))
        self.assertEqual((self.S1 | self.S1).to_value(), (self.S1_value, Operators.OR, self.S1_value))
        self.assertEqual((self.S1 ^ self.S1).to_value(), (self.S1_value, Operators.XOR, self.S1_value))
