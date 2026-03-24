import ast
import math
import operator as op


SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

SAFE_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def safe_factorial(value):
    """Return factorial for non-negative integers only."""
    if isinstance(value, float) and not value.is_integer():
        raise ValueError("Factorial only works with integers.")

    value = int(value)

    if value < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    return math.factorial(value)


def preprocess_expression(expression: str) -> str:
    """Normalize supported symbols before parsing."""
    return (
        expression.replace("^", "**")
        .replace("×", "*")
        .replace("÷", "/")
        .strip()
    )


def build_safe_functions(angle_mode="Radians"):
    """Create allowed math functions."""

    def convert_angle(value):
        if angle_mode == "Degrees":
            return math.radians(value)
        return value

    return {
        "sin": lambda x: math.sin(convert_angle(x)),
        "cos": lambda x: math.cos(convert_angle(x)),
        "tan": lambda x: math.tan(convert_angle(x)),
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
        "factorial": safe_factorial,
        "exp": math.exp,
    }


def _evaluate(node, safe_names, safe_functions):
    """Recursively evaluate the AST."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body, safe_names, safe_functions)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant value.")

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left, safe_names, safe_functions)
        right = _evaluate(node.right, safe_names, safe_functions)
        operator_type = type(node.op)

        if operator_type not in SAFE_OPERATORS:
            raise ValueError("Unsupported operator.")

        return SAFE_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand, safe_names, safe_functions)
        operator_type = type(node.op)

        if operator_type not in SAFE_UNARY_OPERATORS:
            raise ValueError("Unsupported unary operator.")

        return SAFE_UNARY_OPERATORS[operator_type](operand)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call.")

        func_name = node.func.id

        if func_name not in safe_functions:
            raise ValueError(f"Function '{func_name}' is not allowed.")

        args = [_evaluate(arg, safe_names, safe_functions) for arg in node.args]
        return safe_functions[func_name](*args)

    if isinstance(node, ast.Name):
        if node.id in safe_names:
            return safe_names[node.id]
        raise ValueError(f"Unknown name '{node.id}'.")

    raise ValueError("Invalid expression.")


def safe_eval(expression: str, angle_mode="Radians"):
    """Safely evaluate a math expression."""
    expression = preprocess_expression(expression)

    if not expression:
        raise ValueError("Expression cannot be empty.")

    safe_names = {
        "pi": math.pi,
        "e": math.e,
    }

    safe_functions = build_safe_functions(angle_mode)

    try:
        parsed = ast.parse(expression, mode="eval")
        return _evaluate(parsed, safe_names, safe_functions)

    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed.")
    except OverflowError:
        raise ValueError("The result is too large.")
    except SyntaxError:
        raise ValueError("Invalid expression syntax.")
    except TypeError:
        raise ValueError("Invalid function usage.")
    except ValueError as error:
        if "math domain error" in str(error).lower():
            raise ValueError("Invalid input for this mathematical function.")
        raise