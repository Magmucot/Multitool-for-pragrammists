import secrets
from enum import Enum, IntEnum
from math import log2


class Characters(Enum):
    btn_up = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    btn_lower = "abcdefghijklmnopqrstuvwxyz"
    btn_nums = "0123456789"
    btn_spec = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

GENERATE_PASSWORD = (
    'btn_refresh', 'btn_lower', 'btn_up', 'btn_nums', 'btn_spec')
CHARACTER_NUMBER = {
    "btn_lower": len(Characters.btn_lower.value),
    "btn_up": len(Characters.btn_up.value),
    "btn_nums": len(Characters.btn_nums.value),
    "btn_spec": len(Characters.btn_spec.value),
}


class StrengthToEntropy(IntEnum):
    СЛАБЕЙШИЙ = 0
    Слабый = 30
    Норм = 50
    Хороший = 70
    Прекрасный = 120
    БОЖЕСТВЕННЫЙ = 1000


def generate_password(length: int, chars: str) -> str:
    return "".join(secrets.choice(chars) for _ in range(length))


def get_entropy(length: int, chars: int) -> float:
    entropy = length * log2(chars)
    return round(entropy, 3)
