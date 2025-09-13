from tkinter import *
from tkinter import ttk
from hand import Hand
import datetime

class Window:

    def __init__(self):

        TITLE = "blackjack-player-bot"
        BACKGROUND_COLOR = "#292A2D"
        ICON = "images/blackjack-icon.jpg"
        BOT_PIC = "images/bj-player-bot.png"
        FONT = ("Consolas", 16, "bold")
        LABEL_COLOR = "#AD5B27"
        INFO_COLOR = "#EDC380"

        self._starting_bankroll : int = 0
        self._total_earn : float = 0
        self._cards_so_far : int = 0
        self._hands_so_far : int = 0

        # Window
        self._tk = Tk()
        self._tk.config(padx=10, pady=20, background=BACKGROUND_COLOR)
        self._tk.title(TITLE)
        root = self._tk.winfo_toplevel()
        root.geometry("920x550+400+200")
        root.resizable(False, False)
        icon = PhotoImage(file=ICON)
        root.iconphoto(True, icon)
        self._tk.grid_columnconfigure(index=0, minsize=200)
        self._tk.grid_columnconfigure(index=1, minsize=300)

        # Dealer Hand
        self._dealer_hand_lbl = Label(text="Dealer Hand: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._dealer_hand_lbl.grid(column=0, row=0, sticky='e')
        self._dealer_hand = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._dealer_hand.grid(column=1, row=0, sticky='w')

        # Player Hand
        self._player_hand_lbl = Label(text="Player Hand: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._player_hand_lbl.grid(column=0, row=1, sticky='e')
        self._player_hand = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._player_hand.grid(column=1, row=1, sticky='w')

        # Running Count
        self._running_count_lbl = Label(text="Running Count: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._running_count_lbl.grid(column=0, row=2, sticky='e')
        self._running_count = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._running_count.grid(column=1, row=2, sticky='w')

        # True Count
        self._true_count_lbl = Label(text="True Count: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._true_count_lbl.grid(column=0, row=3, sticky='e')
        self._true_count = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._true_count.grid(column=1, row=3, sticky='w')

        separator1 = ttk.Separator(root, orient='horizontal')
        separator1.grid(row=4, column=0, columnspan=2, sticky='ew', padx=0, pady=10)

        # Bankroll
        self._bankroll_lbl = Label(text="Bankroll: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._bankroll_lbl.grid(column=0, row=5, sticky='e')
        self._bankroll = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._bankroll.grid(column=1, row=5, sticky='w')

        # Earn
        self._earn_lbl = Label(text="Earn: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._earn_lbl.grid(column=0, row=6, sticky='e')
        self._earn = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._earn.grid(column=1, row=6, sticky='w')

        # Last result
        self._last_result_lbl = Label(text="Last Result: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._last_result_lbl.grid(column=0, row=7, sticky='e')
        self._last_result= Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._last_result.grid(column=1, row=7, sticky='w')

        # Bet
        self._bet_lbl = Label(text="Current Bet: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._bet_lbl.grid(column=0, row=8, sticky='e')
        self._bet = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._bet.grid(column=1, row=8, sticky='w')

        separator2 = ttk.Separator(root, orient='horizontal')
        separator2.grid(row=9, column=0, columnspan=2, sticky='ew', padx=0, pady=10)

        # Cards seen so far
        self._sofar_cards_lbl = Label(text="Cards so far: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._sofar_cards_lbl.grid(column=0, row=10, sticky='e')
        self._sofar_cards_count = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._sofar_cards_count.grid(column=1, row=10, sticky='w')

        # Hands so far
        self._sofar_hands_lbl = Label(text="Hands so far: ".upper(), font=FONT, fg=LABEL_COLOR, bg=BACKGROUND_COLOR, pady=5)
        self._sofar_hands_lbl.grid(column=0, row=11, sticky='e')
        self._sofar_hands_count = Label(text="Wait", font=FONT, fg=INFO_COLOR, bg=BACKGROUND_COLOR)
        self._sofar_hands_count.grid(column=1, row=11, sticky='w')

        # Bot Image
        bot_png_canvas = Canvas(self._tk, width=400, height=500, highlightthickness=0, background=LABEL_COLOR)
        bot_png_canvas.grid(column=3, row=0, rowspan=12, padx=5)
        bot_pic = PhotoImage(file=BOT_PIC)
        bot_png_canvas.image_ref = bot_pic
        bot_png_canvas.create_image(200, 250, image=bot_pic)


    def set_starting_bankroll(self, bankroll : int):
        self._starting_bankroll = bankroll

    def update_player_hand_and_bet(self, player_hand : Hand):
        self._player_hand.config(text=str(player_hand))
        self._bet.config(text=f"{player_hand.get_bet()}")
        self._tk.update()

    def update_dealer_hand(self, dealer_hand : Hand):
        self._dealer_hand.config(text=str(dealer_hand))
        self._tk.update()

    def update_running_count(self, running_count : int):
        self._running_count.config(text=f"{running_count}")
        self._tk.update()

    def update_true_count(self, true_count : float):
        self._true_count.config(text=f"{round(true_count, 2)}")
        self._tk.update()

    def update_bankroll_and_earn(self, curr_bankroll : float):
        self._bankroll.config(text=f"{curr_bankroll} / {self._starting_bankroll}")
        self._total_earn = curr_bankroll - self._starting_bankroll
        self._earn.config(text=f"{self._total_earn}")
        self._tk.update()

    def update_last_result(self, last_gain : float):
        if last_gain < 0:
            self._last_result.config(text=f"You lost {last_gain}")
        else:
            self._last_result.config(text=f"You won {last_gain}")
        self._tk.update()

    def update_cards_so_far(self, cards_num_to_add : int):
        self._cards_so_far += cards_num_to_add
        self._sofar_cards_count.config(text=self._cards_so_far)
        self._tk.update()

    def update_hands_so_far(self, hands_num_to_add : int):
        self._hands_so_far += hands_num_to_add
        self._sofar_hands_count.config(text=self._hands_so_far)
        self._tk.update()

    def save_report(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"reports/{timestamp}.txt", "w") as report:
            report.write(f"Starting Bankroll: {self._starting_bankroll}\n")
            report.write(f"Total Earn: {self._total_earn}\n")
            report.write(f"Hands: {self._hands_so_far}\n")
            report.write(f"Cards: {self._cards_so_far}\n")

    def mainloop(self):
        self._tk.mainloop()

    def get_root(self):
        return self._tk
