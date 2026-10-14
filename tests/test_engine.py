import unittest
from calculator.engine import CalculatorEngine, CalculationError

class EngineTests(unittest.TestCase):
    def test_operations(self):
        engine = CalculatorEngine()
        for expr, expected in [("2+3*4",14),("(2+3)*4",20),("2^3^2",512),("-2^2",-4),("50/100",.5),("10%3",1),("sin(30)",.5),("acos(0)",90),("sqrt(81)",9),("log(100)",2),("ln(e)",1),("fact(5)",120)]:
            with self.subTest(expr=expr):
                self.assertAlmostEqual(engine.calculate(expr), expected)
        self.assertAlmostEqual(engine.calculate("sin(pi/2)", degrees=False),1)

    def test_rejected_inputs(self):
        for expr in ["", "1/0", "sqrt(-1)", "fact(1.5)", "fact(171)", "(-1)^0.5", "2^1001", "1e999", "sin()", "sin(1,2)", "__import__('os')", "(1).__class__", "[1,2]", "True"]:
            with self.subTest(expr=expr), self.assertRaises(CalculationError):
                CalculatorEngine().calculate(expr)

    def test_answer_after_failure(self):
        engine = CalculatorEngine()
        engine.calculate("6*7")
        with self.assertRaises(CalculationError):
            engine.calculate("1/0")
        self.assertEqual(engine.calculate("ans+1"),43)
