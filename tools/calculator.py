import ast
import operator

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.n if hasattr(node, 'n') else node.value
    elif isinstance(node, ast.BinOp):
        op = SAFE_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {node.op}")
        return op(_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        op = SAFE_OPS.get(type(node.op))
        return op(_eval(node.operand))
    else:
        raise ValueError(f"Unsupported expression: {node}")


def calculate(expression: str) -> dict:
    """
    Safely evaluate a math expression string.
    Returns: {"expression": ..., "result": ..., "error": ...}
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _eval(tree.body)
        return {"expression": expression, "result": result, "error": None}
    except Exception as e:
        return {"expression": expression, "result": None, "error": str(e)}
