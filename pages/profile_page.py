from pages.base_page import BasePage
from config.settings import COORDS

_TAB_NAMES = ["Notifications", "API"]


class ProfilePage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
        self.tag("Profile / Account")
        print("Profile / Account")
        self.click_coord(COORDS["sidebar"]["profile"])
        self.wait_ms(2_000)
        result = [("Profile / Account", self.screenshot())]

        for name, coord in zip(_TAB_NAMES, COORDS["profile_tabs"]):
            self.tag(f"Profile / {name}")
            print(f"Profile / {name}")
            self.click(*coord)
            self.wait_ms(2_500)
            result.append((f"Profile / {name}", self.screenshot()))
        return result
