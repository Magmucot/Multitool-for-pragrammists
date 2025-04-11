from math import cos, sin, tan, radians, exp, e, sqrt, factorial, cosh, log
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
        elif s.startswith("√"):
            oper, num = s[0], s[1:]
            num = self.easy_math(num)
        elif s.startswith("∫"):
            oper = "∫"
            parts = s[1:].split(", ")
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
        else:
            if s.startswith("|") and s.endswith("|"):
                oper, num = "|", s[1:-1]
            else:
                parts = s.split("(", 1)
                if len(parts) == 2 and parts[0] in opers and parts[1].endswith(")"):
                    oper, num = parts[0], parts[1][:-1]
                else:
                    oper, num = "|", s
            num = self.easy_math(num)

        num = float(num)
        if int(num) == num:
            num = int(num)

        if oper in ["cos", "sin", "tan"]:
            num = radians(num)
        res = opers[oper](num)
        return round(res, 12)

    def easy_math(self, s):
        s = s.replace("−", "-").replace("×", "*")
        if not s:
            raise ValueError("Пустая строка в easy_math")
        return eval(s)

    def combined_calc(self, s):
        try:
            s = s.replace(" ", "").replace("^", "**")
            pat = r"""(√(?:\d+(?:\.\d+)?|pi|e))
            |((?:\d+(?:\.\d+)?|pi|e)!)
            |(∫[a-z]+,(?:\d+(?:\.\d+)?|pi|e),(?:\d+(?:\.\d+)?|pi|e))
            |([a-z]{3})\((?:\d+(?:\.\d+)?|pi|e|\d+[-+*/]\d+)\)
            |(log)\((?:\d+(?:\.\d+)?|pi|e|\d+[-+*/**]\d+)(?:,(?:\d+(?:\.\d+)?|pi|e))?\)"""
            while re.search(pat, s):
                match = re.search(pat, s)
                part = match.group(0)
                if match.group(4):
                    func, inr = match.group(4), match.group(5)
                    inner_res = self.easy_math(inr)
                    res = self.diff_math_function(f"{func}({inner_res})")
                else:
                    res = self.diff_math_function(part)
                if res == int(res):
                    res = int(res)
                s = s[: match.start()] + str(res) + s[match.end() :]

            return self.easy_math(s)
        except Exception as e:
            return f"Ошибка: {e}"
calc = Calculator()
print(str(calc.combined_calc('log(10)')))