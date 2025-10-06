# core/calculator.py
import math
from decimal import Decimal, getcontext
from .history import History

getcontext().prec = 50
history = History()

def evaluate(expr: str):
    allowed = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed.update({
        'abs': abs, 'round': round, 'max': max, 'min': min,
        'pi': math.pi, 'e': math.e,
        'sqrt': math.sqrt, 'log': math.log, 'ln': math.log,
        'log10': math.log10, 'exp': math.exp,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'radians': math.radians, 'degrees': math.degrees,
        'ceil': math.ceil, 'floor': math.floor,
        'Decimal': Decimal
    })

    try:
        code = compile(expr, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed:
                raise NameError(f"Запрещённая функция: {name}")
        result = eval(code, {"__builtins__": {}}, allowed)
        history.add(expr, result)
        return result
    except Exception as e:
        raise ValueError(f"Ошибка: {e}")

def get_history():
    return history.get_all()

def clear_history():
    history.clear()