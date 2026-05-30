from pages.base_page import BasePage
from config.settings import COORDS


class CardsPage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
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

        self.tag("Cards / Card Credentials")
        print("Cards / Card Credentials")
        self.click(*COORDS["header"]["card_credentials"])
        self.wait_ms(5_000)
        creds_screenshot = ("Cards / Card Credentials", self.screenshot())
        self.click_coord(COORDS["header"]["close"])
        self.wait_ms(1_000)

        return [
            ("Cards", self.screenshot()),
            creds_screenshot,
        ]
