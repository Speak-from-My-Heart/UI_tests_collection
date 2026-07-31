from pages.base_page import BasePage
from config.settings import COORDS

_TAB_NAMES = ["Transfers", "Balance History"]


class AccountsPage(BasePage):

    def visit(self) -> list[tuple[str, bytes]]:
        self.click_coord(COORDS["sidebar"]["accounts"])
        self.wait_ms(10_000)

        _tab_wait = {"Balance History": 24_000}

        result = []
        for name, coord in zip(_TAB_NAMES, COORDS["accounts_tabs"]):
            self.tag(f"Accounts / {name}")
            print(f"Accounts / {name}")
            self.click(*coord)
            self.wait_ms(4_000)  # ждём пока запрос уйдёт
            self.wait_network(timeout=90_000)  # ждём networkidle до 90 сек
            self.wait_ms(_tab_wait.get(name, 6_000))  # буфер для Flutter-рендера
            result.append((f"Accounts / {name}", self.screenshot()))
        return result
