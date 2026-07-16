from pages.base_page import BasePage
from config.settings import COORDS

_TAB_NAMES = ["Transfers", "Balance History"]


class AccountsPage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
        self.click_coord(COORDS["sidebar"]["accounts"])
        self.wait_ms(2_000)

        _tab_wait = {"Balance History": 8_000}

        result = []
        for name, coord in zip(_TAB_NAMES, COORDS["accounts_tabs"]):
            self.tag(f"Accounts / {name}")
            print(f"Accounts / {name}")
            self.click(*coord)
            self.wait_ms(_tab_wait.get(name, 2_500))
            result.append((f"Accounts / {name}", self.screenshot()))
        return result
