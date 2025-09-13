from card import Card

class Hand:
    def __init__(self):
        self._card_list: list [Card] = []
        self._bet: float = 0

    def __str__(self):
        return " ".join([str(card) for card in self._card_list])

    def add_card(self, card : Card):
        self._card_list.append(card)

    def add_cards(self, cards : list[Card]):
        for card in cards:
            self._card_list.append(card)

    def pop_card(self) -> Card:
        return self._card_list.pop()

    def card_list(self) -> list[Card]:
        return self._card_list

    def hard_total(self) -> int:
        hand_value = sum([card.get_int_value() for card in self._card_list])
        ace_count = len([card for card in self._card_list if card.get_value() == "A"])

        while hand_value > 21 and ace_count > 0:
            hand_value -= 10
            ace_count -= 1

        return hand_value

    def soft_total(self) -> int:
        hand_values = [card.get_value() for card in self._card_list]

        if "A" in hand_values:
            ace_index = hand_values.index("A")
            hand_values.pop(ace_index)

            tot: int = 0
            for value in hand_values:
                if value == "A":
                    tot += 1
                elif value in ["K", "Q", "J"]:
                    tot += 10
                else:
                    tot += int(value)

            return tot + 1

        return self.hard_total()

    def set_bet(self, bet : int):
        self._bet = bet

    def get_bet(self) -> float:
        return self._bet

    def double_bet(self):
        self._bet *= 2

    def is_soft(self) -> bool:
        if self.soft_total() < self.hard_total():
            return True
        return False

    def is_pair(self) -> bool:
        cards = self._card_list
        if len(cards) == 2 and cards[0].get_value() == cards[1].get_value():
            return True
        return False

    def busted(self):
        if self.hard_total() > 21 and self.soft_total() > 21:
            return True
        return False
