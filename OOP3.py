from math import cos, sin, tan, radians, exp, e, sqrt, factorial, cosh, log, pi, fabs, acos, acosh, asin, atan
from scipy.integrate import nquad
from operator import abs as abs_op
import re


class Calculator:
        def __init__(self):
            self.sp_opers = []
            self.sp_nums = []

        def diff_math_function(self, s):
            s = s.strip()
            opers = {
                'log':log,
                'arccos': acos,
                "arccosh": acosh,
                "arcsin": asin,
                "arctan": atan,
                "|": abs_op,
                "cosh": cosh,
                "cos": cos,
                "sin": sin,
                "tan": tan,
                "!": factorial,
                "√": sqrt,
                "∫": nquad,
            }

            if s.endswith("!"):
                oper, num = s[-1], s[:-1]
                num = self.easy_math(num)
            elif s.startswith("|") and s.endswith("|"):
                inner_expr = s[1:-1]
                inner_res = self.combined_calc(inner_expr)
                num = float(inner_res)
                return fabs(num)
            elif s.startswith("√"):
                num_str = s[1:]
                if num_str == "pi":
                    num = pi
                elif num_str == "e":
                    num = e
                else:
                    num = float(num_str)
                if num < 0:
                    raise ValueError("Корень из отрицательного числа")
                return sqrt(num)
            elif s.startswith('log'):
                s = s[4:-1]
                if ',' in s:
                    num, base = map(float, s.split(','))
                else:
                    base = e
                return log(num, base)
            elif s.startswith("∫"):
                oper = "∫"
                parts = s[2:-1].split(",")
                func_str, a, b = parts[0], float(parts[1]), float(parts[2])
                func_map = {
                    "sin": sin,
                    "cos": cos,
                    "tan": tan,
                    "cosh": cosh,
                    "sqrt": sqrt,
                    "log": lambda x: log(x, e),
                    "exp": exp,
                }
                result = opers[oper](func_map[func_str], [(a, b)])[0]
                return round(result, 12)
            elif s.startswith("|") and s.endswith("|"):
                oper, num = "|", s[1:-1]
            elif '(' in s:
                if s.endswith(')'):
                    s = s[:-1]
                oper, num = s.split('(')
            else:
                return self.easy_math(s)

            num = float(num)
            if int(num) == num:
                num = int(num)

            if oper in ["cos", "sin", "tan", 'arccos', "arccosh", "arcsin", "arctan", 'ctg']:
                num = radians(num)

            if oper == 'ctg':
                return cos(num) / sin(num)
            res = opers[oper](num)

            return round(res, 12)

        def easy_math(self, s):
            s = s.replace("^", "**").replace("×",
                                            "*").replace("÷", '/').replace("−", "-")
            if not s:
                raise ValueError("Пустая строка в easy_math")
            return eval(s)

        def combined_calc(self, s):
            try:
                s = s.replace(" ", "")
                pat = r"""(√(\(?)(?:-?\d*\.?\d+|pi|e)(\)?))
                |(\|[^|]+\|)
                |((?:-?\d*\.?\d+|pi|e)!)
                |((\∫)(\(?)([a-z]+,(?:\d+(?:\.\d+)?|pi|e),(?:\d+(?:\.\d+)?|pi|e)(\)?))
                |((?:arc)?[a-z]{3})(\(-?\d*\.?\d+|pi|e|-?\d+[-+*/%//]\d|pi|e+)\))
                |(log)\((?:-?\d*\.?\d+|pi|e|-?\d+[-+*/**]\d+)(?:,-?\d*\.?\d+)?\)"""
                while re.search(pat, s, re.VERBOSE):
                    match = re.search(pat, s, re.VERBOSE)
                    part = match.group(0)
                    res = self.diff_math_function(part)
                    if res == int(res):
                        res = int(res)
                    s = s[: match.start()] + str(res) + s[match.end():]

                return self.easy_math(s)
            except Exception as e:
                return f"Ошибка: {e}"
