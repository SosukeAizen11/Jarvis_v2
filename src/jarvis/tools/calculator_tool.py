import ast
import operator


class CalculatorTool:
    """Safely evaluates basic arithmetic expressions."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    def execute(self, expression: str) -> str:
        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)
            return str(result)

        except Exception:
            return "Invalid mathematical expression."

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            operator_func = self.OPERATORS[type(node.op)]

            return operator_func(left, right)

        raise ValueError("Unsupported expression.")