"""
monitor.py — главный файл запуска.

Здесь только оркестрация: создаём объекты, обходим страницы,
собираем скриншоты, отправляем отчёт ТОЛЬКО если есть ошибки.

Локально:   python monitor.py
В CI:       python monitor.py  (креды приходят из GitHub Secrets через env:)
"""

import sys
from config.settings import SITES
from core.browser import BrowserManager
from core.error_collector import ErrorCollector
from notifications.telegram_notifier import TelegramNotifier
from reports.report_builder import ReportBuilder

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.accounts_page import AccountsPage
from pages.cards_page import CardsPage
from pages.payments_page import PaymentsPage
from pages.refunds_page import RefundsPage
from pages.top_ups_page import TopUpsPage
from pages.balance_summary_page import BalanceSummaryPage


def run_monitor(headless: bool = True) -> None:
    notifier = TelegramNotifier()

    for site in SITES:
        print(f"\n{'='*40}\nЗапуск для: {site['name']}\n{'='*40}")

        collector   = ErrorCollector()
        screenshots = []

        with BrowserManager(headless=headless) as bm:
            bm.page.on("response", collector.on_response)

            login = LoginPage(bm, collector, site)   # ← передаём site
            login.open()
            login.login()
            screenshots.append(("После логина", login.screenshot()))

            # ── 2. Home / Deposit ─────────────────────────────────────────────────
            home = HomePage(bm, collector)
            home.visit()
            screenshots.append(("Home / Deposit", home.screenshot()))

            # ── 3. Accounts ───────────────────────────────────────────────────────
            accounts = AccountsPage(bm, collector)
            accounts.visit()
            screenshots.append(("Accounts", accounts.screenshot()))

            # ── 4. Cards ──────────────────────────────────────────────────────────
            cards = CardsPage(bm, collector)
            cards.visit()
            screenshots.append(("Cards", cards.screenshot()))

            # ── 5. Payments ───────────────────────────────────────────────────────
            payments = PaymentsPage(bm, collector)
            payments.visit()
            screenshots.append(("Payments", payments.screenshot()))

            # ── 6. Refunds ────────────────────────────────────────────────────────
            refunds = RefundsPage(bm, collector)
            refunds.visit()
            screenshots.append(("Refunds", refunds.screenshot()))

            # ── 7. Top Ups ────────────────────────────────────────────────────────
            top_ups = TopUpsPage(bm, collector)
            top_ups.visit()
            screenshots.append(("Top Ups", top_ups.screenshot()))

            # ── 8. Balance Summary ────────────────────────────────────────────────
            balance = BalanceSummaryPage(bm, collector)
            balance.visit()
            screenshots.append(("Balance Summary", balance.screenshot()))

            report = ReportBuilder(collector, site["name"])

            if report.has_errors():
                print(f"[{site['name']}] Найдено ошибок: {collector.total()}")
                notifier.send_report_with_screenshots(report.build(), screenshots)
            else:
                print(f"[{site['name']}] Ошибок не найдено ✅")
                notifier.send_text(report.build_ok_message())

    # ── Отчёт ─────────────────────────────────────────────────────────────────

    print("Мониторинг завершён")


if __name__ == "__main__":
    # Передай --show чтобы запустить с видимым браузером (для отладки локально)
    headless = "--show" not in sys.argv
    run_monitor(headless=headless)

#смотреть координаты document.addEventListener('mousemove', e => console.log(`X: ${e.clientX}, Y: ${e.clientY}`));
