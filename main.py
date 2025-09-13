import time
from bot import Bot
import threading

TIMEOUT_SEC = 60*20 # 20 min (approximately 300 hands)

bot = Bot()

def run_bot_loop():
    end_timer = time.time() + TIMEOUT_SEC

    while time.time() < end_timer and not bot.out_of_money():
        bot.deal()
        time.sleep(0.2)


threading.Thread(target=run_bot_loop, daemon=True).start()

bot.ui_mainloop()
bot.quit()