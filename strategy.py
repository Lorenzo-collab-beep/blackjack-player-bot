import pandas
from hand import Hand
from card import Card

hard_strategy = pandas.read_csv("strategy/hard-hand-strategy.csv", index_col=0)
soft_strategy = pandas.read_csv("strategy/soft-hand-strategy.csv", index_col=0)
pair_strategy = pandas.read_csv("strategy/pair-hand-strategy.csv", index_col=0)


def check_hard_illustrious(current_decision : str, player_hand_value : int, dealer_card_value : int, true_count : float) -> str:
    illustrious_decision : str = current_decision

    if player_hand_value == 16:
        if dealer_card_value == 9 and true_count >= 5:
            illustrious_decision = "S"
        elif dealer_card_value == 10 and true_count >= 0:
            illustrious_decision = "S"

    elif player_hand_value == 15 and dealer_card_value == 10 and true_count >= 4:
        illustrious_decision = "S"

    elif player_hand_value == 13:
        if dealer_card_value == 2 and true_count <= -1:
            illustrious_decision = "H"
        elif dealer_card_value == 3 and true_count <= -2:
            illustrious_decision = "H"

    elif player_hand_value == 12:
        if dealer_card_value == 2 and true_count >= 3:
            illustrious_decision = "S"
        elif dealer_card_value == 3 and true_count >= 2:
            illustrious_decision = "S"
        elif dealer_card_value == 4 and true_count <= 0:
            illustrious_decision = "H"
        elif dealer_card_value == 5 and true_count <= -2:
            illustrious_decision = "H"
        elif dealer_card_value == 6 and true_count <= -1:
            illustrious_decision = "H"

    elif player_hand_value == 11:
        if dealer_card_value == 10 and true_count >= 4:
            illustrious_decision = "D"
        elif dealer_card_value == 11 and true_count >= 1:
            illustrious_decision = "D"

    elif player_hand_value == 10:
        if dealer_card_value == 9 and true_count <= -1:
            illustrious_decision = "H"
        elif (dealer_card_value == 10 or dealer_card_value == 11) and true_count >= 4:
            illustrious_decision = "D"

    elif player_hand_value == 9:
        if dealer_card_value == 2 and true_count >= 1:
            illustrious_decision = "D"
        elif dealer_card_value == 7 and true_count >= 3:
            illustrious_decision = "D"

    return illustrious_decision

def check_soft_illustrious(current_decision : str, player_no_ace_value : int, dealer_card_value : int, true_count : float) -> str:
    illustrious_decision: str = current_decision

    if player_no_ace_value == 7:
        if dealer_card_value == 11 and true_count >= 1:
            illustrious_decision = "S"

    return illustrious_decision

def check_pair_illustrious(current_decision: str, player_pair_value: int, dealer_card_value: int, true_count: float) -> str:
    illustrious_decision: str = current_decision

    if player_pair_value == 10:
        if dealer_card_value == 6 and true_count >= 4:
            illustrious_decision = "P"
        elif dealer_card_value == 5 and true_count >= 5:
            illustrious_decision = "P"

    return illustrious_decision

def get_hard_hand_decision(dealer_card_value : int, player_hand_total : int, true_count : float) -> str:
    if player_hand_total >= 17:
        decision = "S"
    elif player_hand_total <= 7:
        decision = "H"
    else:
        decision = hard_strategy.get(str(dealer_card_value))[player_hand_total]

    decision = check_hard_illustrious(decision, player_hand_total, dealer_card_value, true_count)

    return decision

def get_soft_hand_decision(dealer_card_value : int, player_hand_total_no_ace : int, true_count : float) -> str:
    if player_hand_total_no_ace > 8:
        decision = "S"
    elif player_hand_total_no_ace < 6:
        decision = "H"
    else:
        decision = soft_strategy.get(str(dealer_card_value))[player_hand_total_no_ace]

    decision = check_soft_illustrious(decision, player_hand_total_no_ace, dealer_card_value, true_count)

    return decision

def get_correct_decision(player_hand : Hand, dealer_card : Card, true_count : float, max_money : float, split_times : int) -> str:
    dealer_c = dealer_card.get_int_value()
    player_bet = player_hand.get_bet()
    hard_total = player_hand.hard_total()
    soft_total_no_ace = player_hand.soft_total() - 1

    # print(player_hand)

    if player_hand.is_pair():
        pair_value = player_hand.card_list()[0].get_int_value()
        decision = pair_strategy.get(str(dealer_c))[pair_value]

        decision = check_pair_illustrious(decision, pair_value, dealer_c, true_count)

        if decision != "P":
            decision = check_hard_illustrious(decision, player_hand.hard_total(), dealer_c, true_count)

    elif player_hand.is_soft():
        decision = get_soft_hand_decision(dealer_c, soft_total_no_ace, true_count)

    else:
        decision = get_hard_hand_decision(dealer_c, hard_total, true_count)


    if decision == "D" and (player_bet * 2 > max_money or len(player_hand.card_list()) > 2 or split_times > 0):
        decision = "H"

    if decision == "P":
        if ((split_times + 1) * player_bet) + player_bet > max_money or split_times == 3:
            if player_hand.is_soft():
                decision = get_soft_hand_decision(dealer_c, soft_total_no_ace, true_count)
            else:
                decision = get_hard_hand_decision(dealer_c, hard_total, true_count)

    # print(decision)
    return decision
