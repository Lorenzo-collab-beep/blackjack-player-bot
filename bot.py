from strategy import get_correct_decision
from gamedriver import Gamedriver
from card import Card
from hand import Hand
from ui import Window
import tkinter as tk
import time

RED_CHIP_AMOUNT = 25
GREEN_CHIP_AMOUNT = 10
BLUE_CHIP_AMOUNT = 5
BLACK_CHIP_AMOUNT = 1


class Bot:

    def __init__(self):

        self._ui = Window()
        self._gamedriver = Gamedriver()

        self._current_bet = 0
        self._minimum_bet = self._gamedriver.scrape_table_minimum()

        self._split_flag : int = 0 #splits still to manage
        self._split_times : int = 0 #splits tot in current deal

        self._player_hands : list[Hand] = []
        self._player_hand_idx : int = 0
        self._dealer_hand : Hand = Hand()

        self._game_decks : int = int(self._gamedriver.scrape_remaining_decks())
        self._tot_decks = self._game_decks

        self._bankroll : float = self._gamedriver.scrape_bankroll()
        self._ui.set_starting_bankroll(int(self._bankroll))
        self._ui.update_bankroll_and_earn(self._bankroll)

        self._running_count : int = 0
        self._true_count : float = 0

        self._current_decision : str = "None"

        self._enable__check_shuffle = False

    def _update_running_count(self, cards_list : list[Card]):
        for card in cards_list:
            card_value = card.get_int_value()
            if card_value >= 10:
                self._running_count -= 1
            elif card_value <= 6:
                self._running_count += 1
        self._ui.update_running_count(self._running_count)

    def _check_shuffle(self):
        if self._enable__check_shuffle and self._gamedriver.scrape_tray_cards() == 0:
            self._running_count = 0
            self._true_count = 0
            self._ui.update_running_count(self._running_count)
            self._ui.update_true_count(self._true_count)

    def _update_true_count(self):
        self._game_decks = float(self._gamedriver.scrape_remaining_decks())

        if self._game_decks != 0:
            self._true_count = self._running_count/self._game_decks

        self._ui.update_true_count(self._true_count)

    def _calculate_bet(self):
        self._current_bet =  int(self._minimum_bet * (1 + self._true_count))

        if self._current_bet < self._minimum_bet:
            self._current_bet = self._minimum_bet

        if self._current_bet > self._bankroll:
            self._current_bet = self._bankroll

    def _execute_bet(self):
        bet_to_do = self._current_bet

        red_chips = int(bet_to_do/RED_CHIP_AMOUNT)
        bet_to_do -= red_chips*RED_CHIP_AMOUNT

        green_chips = int(bet_to_do/GREEN_CHIP_AMOUNT)
        bet_to_do -= green_chips*GREEN_CHIP_AMOUNT

        blue_chips = int(bet_to_do/BLUE_CHIP_AMOUNT)
        bet_to_do -= blue_chips*BLUE_CHIP_AMOUNT

        black_chips = int(bet_to_do/BLACK_CHIP_AMOUNT)

        for i in range(red_chips):
            self._gamedriver.click_red_chip()

        for i in range(green_chips):
            self._gamedriver.click_green_chip()

        for i in range(blue_chips):
            self._gamedriver.click_blue_chip()

        for i in range(black_chips):
            self._gamedriver.click_black_chip()

    def _press_start(self):
        self._gamedriver.click_start_deal_button()

    def _press_new_deal(self):
        self._gamedriver.click_new_game_button()

    def _load_player_hand(self):
        # Add a Hand element to player hands list
        self._player_hands.append(Hand())

        cards = [Card(card_str) for card_str in self._gamedriver.scrape_player_hand(self._player_hand_idx)]

        self._player_hands[self._player_hand_idx].add_cards(cards)
        self._player_hands[self._player_hand_idx].set_bet(self._current_bet)

        self._ui.update_player_hand_and_bet(self._player_hands[self._player_hand_idx])

    def _load_dealer_hand(self):
        self._dealer_hand = Hand()

        self._dealer_hand.add_card(Card(self._gamedriver.scrape_dealer_face_up_card()))

        self._ui.update_dealer_hand(self._dealer_hand)

    def _make_correct_decision(self) -> str:
        decision = get_correct_decision(self._player_hands[self._player_hand_idx],
                                        self._dealer_hand.card_list()[0], self._true_count,
                                        self._bankroll, self._split_times)
        if decision == "S":
            self._gamedriver.click_stand_button()
        elif decision == "H":
            self._gamedriver.click_hit_button()
        elif decision == "D":
            self._gamedriver.click_double_button()
        elif decision == "P":
            self._gamedriver.click_split_button()

            # Increase split times and add a split flag
            self._split_times += 1
            self._split_flag += 1

        return decision

    def _update_player_hand(self):
        # Add the new card to current player Hand
        self._player_hands[self._player_hand_idx].card_list().append(
            Card(self._gamedriver.scrape_player_recent_card(self._player_hand_idx)))

        self._ui.update_player_hand_and_bet(self._player_hands[self._player_hand_idx])

    def _wait_for_keypress(self):
        # This function can be useful for debug purpose
        root = self._ui.get_root()
        key_pressed = tk.BooleanVar()

        def on_key(event):
            print(event)
            key_pressed.set(True)

        root.bind("<Key>", on_key)
        root.wait_variable(key_pressed)
        root.unbind("<Key>")

    def _split_hand(self):
        # Check shuffle (dealer gave player new cards)
        self._check_shuffle()

        # Remove a pair card from player hand and load the new card
        self._player_hands[self._player_hand_idx].card_list().pop()
        self._update_player_hand()

        # Update count based on new card
        self._update_running_count([self._player_hands[self._player_hand_idx].card_list()[-1]])
        self._update_true_count()

    def _manage_split_deal(self):
        
        if self._player_hands[0].card_list()[0].get_value() == "A":
            
            # If Bot player split aces it is
            # forced to stand on both new hands

            # Check shuffle (dealer gave player new cards)
            self._check_shuffle()
            
            # Remove a pair card from player hand and load the new card
            self._player_hands[self._player_hand_idx].card_list().pop()
            self._update_player_hand()
            
            # Load the next hand
            self._player_hand_idx += 1
            self._load_player_hand()
            
            # Update counts
            self._update_running_count([self._player_hands[0].card_list()[-1]] 
                                      + [self._player_hands[1].card_list()[-1]])
            self._update_true_count()
            
        else:

            self._split_hand()
    
            while True:
    
                # Do correct decision
                self._current_decision = self._make_correct_decision()
    
                if self._current_decision == "P":
                    self._split_hand()
                    
                elif self._current_decision == "H":
                    # check shuffle if player get a card
                    self._check_shuffle()
    
                    # Add new card to player hand
                    self._update_player_hand()
    
                    # Update count based on new card
                    self._update_running_count([self._player_hands[self._player_hand_idx].card_list()[-1]])
                    self._update_true_count()
                    
                if self._current_decision == "S" or self._player_hands[self._player_hand_idx].busted():
                    if self._split_flag > 0:
                        
                        # Load player next hand
                        self._player_hand_idx += 1
                        self._load_player_hand()

                        # Update count
                        self._update_running_count([self._player_hands[self._player_hand_idx].card_list()[-1]])
                        self._update_true_count()
                        
                        # Decrease split flag
                        self._split_flag -= 1
                    else:
                        break

                time.sleep(0.2)
                # # Wait till user press a key (for test purpose)
                # self._wait_for_keypress() #TODO: remove

    def deal(self):
        # Reset things
        self._player_hands = []
        self._player_hand_idx = 0
        self._split_times = 0
        self._split_flag = 0

        # check shuffle in a new turn
        self._check_shuffle()

        # Make a bet
        self._calculate_bet()
        self._execute_bet()
        time.sleep(0.2)

        # Start the game
        self._press_start()

        # Load dealer and player hands
        self._load_dealer_hand()
        self._load_player_hand()

        # check shuffle (dealer just gave cards)
        self._check_shuffle()

        # Update running count
        self._update_running_count(self._player_hands[0].card_list() + self._dealer_hand.card_list())

        # Compute true count
        self._update_true_count()

        while True:

            # Do correct decision
            self._current_decision = self._make_correct_decision()

            if self._current_decision == "P":
                self._manage_split_deal()
                break

            elif self._current_decision == "D" or self._current_decision == "H":
                # check shuffle if player get cards
                self._check_shuffle()

                # Add new card to player hand
                self._update_player_hand()

                # Update count based on new card
                self._update_running_count([self._player_hands[0].card_list()[-1]])
                self._update_true_count()

                # Force stand if Bot pressed double
                if self._current_decision == "D":
                    self._current_decision = "S"

            if self._current_decision == "S" or self._player_hands[0].busted():
                break

            time.sleep(0.2)

        # Wait dealer to end
        self._gamedriver.wait_dealer_turn()

        # check shuffle alter dealer turn
        self._check_shuffle()

        # Add remaining cards to dealer Hand
        self._dealer_hand.add_cards([Card(card) for card in self._gamedriver.scrape_dealer_remaining_cards()])
        self._ui.update_dealer_hand(self._dealer_hand)

        # Update counts
        self._update_running_count(self._dealer_hand.card_list()[1:])
        self._update_true_count()

        # Check gain
        gain = self._gamedriver.scrape_hand_gain()
        self._bankroll += gain
        self._ui.update_bankroll_and_earn(self._bankroll)

        # Update last result
        self._ui.update_last_result(gain)

        # Update Hand tot
        self._ui.update_hands_so_far(len(self._player_hands))

        # Update card tot
        self._ui.update_cards_so_far(sum(len(hand.card_list()) for hand in self._player_hands)
                                     + len(self._dealer_hand.card_list()))

        # Wait till user press a key (for test purpose)
        # self._wait_for_keypress() #TODO: remove

        # Press new deal
        self._press_new_deal()

        # Enable check shuffle after fist deal
        self._enable__check_shuffle = True

    def out_of_money(self) -> bool:
        if self._bankroll == 0:
            return True
        return False

    def ui_mainloop(self):
        self._ui.mainloop()

    def quit(self):
        self._gamedriver.quit()
        self._ui.save_report()
