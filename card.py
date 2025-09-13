
class Card:
    # card_name format samples 2-C, K-H, A-D....
    def __init__(self, card_name : str):
        self._value = card_name.split("-")[0]
        self._int_value = convert_to_integer_value(self._value)
        self._suit = card_name.split("-")[1]
        self._suit_symbol = get_suit_symbol_by_acronym(self._suit)

    def __str__(self):
        return f"{self._value}{self._suit_symbol}"

    def get_value(self) -> str:
        return self._value

    def get_int_value(self) -> int:
        return self._int_value

    def get_suit_symbol(self) -> str:
        return self._suit_symbol


def convert_to_integer_value(value : str) -> int:
    if value in ["K", "J", "Q"]:
        return 10
    elif value == "A":
        return 11

    return int(value)

def get_suit_symbol_by_acronym(acronym: str) -> str or None:
    if acronym == "C":
        return "♣"
    elif acronym == "D":
        return "♦"
    elif acronym == "H":
        return "♥"
    elif acronym == "S":
        return "♠"

    return None
