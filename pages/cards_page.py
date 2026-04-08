"""
CardsPage — раздел Cards.
"""

from pages.base_page import BasePage
from config.settings import COORDS


class CardsPage(BasePage):

    def visit(self) -> None:
        self.tag("Cards")
        print("Cards")
        self.click_coord(COORDS["sidebar"]["cards"])
        self.wait_ms(2_000)
        self.click(*COORDS["cards_tab"])
        self.wait_ms(3_500)
        self.click_coord(COORDS["header"]["close"])
        self.wait_ms(2_000)
        self.click(*COORDS["show_card"])
        self.wait_ms(5_000)
        self.click(*COORDS["header"]["card_credentials"])
        self.wait_ms(5_000)
        self.click_coord(COORDS["header"]["close"])
        self.wait_ms(1_000)
