# solvers/equation_solver.py
from sympy import symbols, Eq, solve, parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

x, y, z = symbols('x y z')

def solve_equation(input_str: str):
    try:
        lines = [line.strip() for line in input_str.split('\n') if line.strip()]
        if len(lines) == 1:
            # Одно уравнение
            eq_str = lines[0]
            if '=' not in eq_str:
                raise ValueError("Уравнение должно содержать '='")
            left, right = eq_str.split('=', 1)
            transformations = standard_transformations + (implicit_multiplication_application,)
            left_expr = parse_expr(left.strip(), transformations=transformations)
            right_expr = parse_expr(right.strip(), transformations=transformations)
            equation = Eq(left_expr, right_expr)
            solutions = solve(equation, x)
            if not solutions:
                return ["Нет решений"]
            return [str(sol.evalf()) for sol in solutions]
        else:
            # Система уравнений
            equations = []
            transformations = standard_transformations + (implicit_multiplication_application,)
            for line in lines:
                if '=' not in line:
                    raise ValueError(f"Уравнение '{line}' должно содержать '='")
                left, right = line.split('=', 1)
                left_expr = parse_expr(left.strip(), transformations=transformations)
                right_expr = parse_expr(right.strip(), transformations=transformations)
                equations.append(Eq(left_expr, right_expr))
            solutions = solve(equations, (x, y, z))
            if not solutions:
                return ["Нет решений"]
            if isinstance(solutions, list):
                return [str(sol) for sol in solutions]
            else:
                return [str(solutions)]
    except Exception as e:
        return [f"Ошибка: {e}"]