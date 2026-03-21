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
        self.wait_ms(1_500)
        self.click_coord(COORDS["header"]["close"])
        self.wait_ms(1_000)
