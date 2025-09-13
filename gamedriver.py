import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import sys
import os


def get_abs_path(filename : str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, filename)

class Gamedriver:
    def __init__(self):
        GAME_URL = get_abs_path("blackjack-game/index.html")

        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option("detach", True)
        chrome_option.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=chrome_option)
        driver.get(GAME_URL)

        self._driver = driver

    def quit(self):
        self._driver.quit()

    def click_start_deal_button(self):
        self.click_button("play-button")

    def click_black_chip(self):
        self.click_button("js-bet1-button")

    def click_blue_chip(self):
        self.click_button("js-bet2-button")

    def click_green_chip(self):
        self.click_button("js-bet3-button")

    def click_red_chip(self):
        self.click_button("js-bet4-button")

    def click_hit_button(self):
        self.click_button("hit-button")

    def click_stand_button(self):
        self.click_button("stand-button")

    def click_double_button(self):
        self.click_button("double-button")

    def click_split_button(self):
        self.click_button("split-button")

    def click_new_game_button(self):
        self.click_button("new-game-button")

    def click_button(self, class_name : str):
        wait = WebDriverWait(self._driver, 10)
        button = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, class_name)))
        button.click()

    def scrape_remaining_decks(self) -> float:
        self.wait_for_element(By.XPATH, "/ html / body / main / div[1] / section[1] / div[2] / div / p")
        return float(self._driver.find_element(By.XPATH, value=""
        "/ html / body / main / div[1] / section[1] / div[2] / div / p").text.split(" ")[2].split(")")[0])

    def scrape_tray_cards(self) -> float:
        self.wait_for_element(By.XPATH, "/ html / body / main / div[1] / section[1] / div[3] / div / p")
        return int(self._driver.find_element(By.XPATH, value=""
        "/ html / body / main / div[1] / section[1] / div[3] / div / p").text.split(" ")[0])

    def scrape_bankroll(self) -> float:
        self.wait_for_element(By.XPATH, "/ html / body / main / div[1] / section[1] / div[7] / div / p")
        return float(int(self._driver.find_element(By.XPATH, value=""
        "/ html / body / main / div[1] / section[1] / div[7] / div / p").text.split(" ")[0]))

    def scrape_table_minimum(self) -> int:
        self.wait_for_element(By.CLASS_NAME, "js-table-minimum")
        return int(self._driver.find_element(By.CLASS_NAME, value="js-table-minimum").text)

    def scrape_player_cards(self, hand_class : str) -> list[str]:
        self.wait_for_element(By.CLASS_NAME, hand_class)
        player_hand = self._driver.find_element(By.CLASS_NAME, value=hand_class)
        player_cards = player_hand.find_elements(By.CLASS_NAME, value="playing-card")
        return list([card.get_attribute("src").split("/")[11].split(".")[0] for card in player_cards
                     if "card-back" not in card.get_attribute("class")])

    def scrape_player_hand(self, hand_idx : int) -> list[str]:
        return self.scrape_player_cards(f"js-player-cards-{hand_idx}")

    def scrape_player_recent_card(self, hand_idx) -> str:
        return self.scrape_player_hand(hand_idx)[-1]

    def scrape_dealer_cards(self) -> list[str]:
        self.wait_for_element(By.CLASS_NAME, "dealer-cards")
        dealer_hand = self._driver.find_element(By.CLASS_NAME, value="dealer-cards")
        dealer_hand = dealer_hand.find_elements(By.CLASS_NAME, value="playing-card")
        return list([card.get_attribute("src").split("/")[11].split(".")[0] for card in dealer_hand
                     if "card-back" not in card.get_attribute("class")])

    def scrape_dealer_face_up_card(self) -> str:
        return self.scrape_dealer_cards()[-1]

    def scrape_dealer_remaining_cards(self) -> list[str]:
        return self.scrape_dealer_cards()[1:]

    def wait_dealer_turn(self):
        self.wait_for_element(By.CLASS_NAME, "result")
        title = str(self._driver.find_element(By.CLASS_NAME, value="result").text)

        while "Game" in title or "Player Busted!" in title:
            time.sleep(0.5)
            self.wait_for_element(By.CLASS_NAME, "result")
            title = str(self._driver.find_element(By.CLASS_NAME, value="result").text)

    def scrape_hand_gain(self):
        self.wait_for_element(By.CLASS_NAME, "js-last-hand-gain")
        return float(self._driver.find_element(By.CLASS_NAME, value="js-last-hand-gain").text.split(" ")[0])

    def wait_for_element(self, by, value, timeout=10):
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(ec.presence_of_element_located((by, value)))
