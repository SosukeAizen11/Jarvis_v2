import ast
import operator

from jarvis.tools.base import BaseTool


class CalculatorTool(BaseTool):
    """Safely evaluates basic arithmetic expressions."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Performs basic arithmetic calculations."
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate.",
                }
            },
            "required": ["expression"],
        }

    def execute(self, arguments: str = "") -> str:
        """Evaluate a mathematical expression safely."""
        try:
            tree = ast.parse(arguments, mode="eval")
            result = self._evaluate(tree.body)
            return str(result)

        except Exception:
            return "Invalid mathematical expression."

    def _evaluate(self, node: ast.AST) -> int | float:
        """Recursively evaluates a parsed AST node."""

        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("Only numeric values are allowed.")
            return node.value

        if isinstance(node, ast.BinOp):
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            operator_func = self.OPERATORS.get(type(node.op))

            if operator_func is None:
                raise ValueError("Unsupported operator.")

            return operator_func(left, right)

        raise ValueError("Unsupported expression.")