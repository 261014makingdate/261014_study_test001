"""Evaluate an explicitly allowed arithmetic syntax without executing code."""
import ast
import math
import operator


class CalculationError(ValueError):
    """A readable calculation failure."""


class CalculatorEngine:
    def __init__(self):
        self._answer = 0.0

    def calculate(self, expression: str, *, degrees: bool = True) -> float:
        if len(expression) > 500:
            raise CalculationError("수식이 너무 깁니다.")
        functions = {
            "sqrt": math.sqrt, "ln": math.log, "log": math.log10,
            "abs": abs, "exp": math.exp, "fact": self._factorial,
        }
        for name in ("sin", "cos", "tan"):
            function = getattr(math, name)
            functions[name] = lambda x, f=function: f(math.radians(x) if degrees else x)
        for name in ("asin", "acos", "atan"):
            function = getattr(math, name)
            functions[name] = lambda x, f=function: math.degrees(f(x)) if degrees else f(x)
        constants = {"pi": math.pi, "e": math.e, "ans": self._answer}
        binary = {ast.Add: operator.add, ast.Sub: operator.sub,
                  ast.Mult: operator.mul, ast.Div: operator.truediv,
                  ast.Pow: self._power, ast.Mod: operator.mod}

        def visit(node):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                if abs(node.value) > 1e100:
                    raise CalculationError("숫자가 허용 범위를 초과했습니다.")
                return float(node.value)
            if isinstance(node, ast.Name) and node.id in constants:
                return constants[node.id]
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                return visit(node.operand) * (-1 if isinstance(node.op, ast.USub) else 1)
            if isinstance(node, ast.BinOp) and type(node.op) in binary:
                return binary[type(node.op)](visit(node.left), visit(node.right))
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in functions and len(node.args) == 1 and not node.keywords):
                return functions[node.func.id](visit(node.args[0]))
            raise CalculationError("지원하지 않는 수식입니다.")

        try:
            normalized = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
            tree = ast.parse(normalized.strip(), mode="eval")
            if sum(1 for _ in ast.walk(tree)) > 150:
                raise CalculationError("수식이 너무 복잡합니다.")
            result = visit(tree.body)
            if not math.isfinite(result):
                raise CalculationError("결과가 허용 범위를 초과했습니다.")
        except CalculationError:
            raise
        except ZeroDivisionError as exc:
            raise CalculationError("0으로 나눌 수 없습니다.") from exc
        except (ValueError, OverflowError, SyntaxError, RecursionError, TypeError) as exc:
            raise CalculationError("수식 또는 함수의 입력 범위를 확인하세요.") from exc
        self._answer = result
        return result

    @staticmethod
    def _power(base, exponent):
        if abs(exponent) > 1000:
            raise CalculationError("지수의 절댓값은 1000 이하여야 합니다.")
        result = base ** exponent
        if isinstance(result, complex):
            raise CalculationError("실수 결과만 지원합니다.")
        return result

    @staticmethod
    def _factorial(value):
        if not value.is_integer() or not 0 <= value <= 170:
            raise CalculationError("팩토리얼은 0~170 정수만 지원합니다.")
        return float(math.factorial(int(value)))
