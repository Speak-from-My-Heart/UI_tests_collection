"""
ReportBuilder — собирает финальный текст отчёта из секций ErrorCollector.
"""

import time
from core.error_collector import ErrorCollector


class ReportBuilder:
    # Все разделы в порядке обхода
    SECTIONS = [
        "Login",
        "Home / Deposit",
        "Accounts",
        "Cards",
        "Payments",
        "Refunds",
        "Top Ups",
        "Balance Summary",
    ]

    def __init__(self, collector: ErrorCollector, site_name: str = ""):
        self.collector  = collector
        self.site_name  = site_name

    def build(self) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        lines = [f"*Отчёт проверки {self.site_name} {timestamp}*\n"]

        for section in self.SECTIONS:
            lines.append(self.collector.format_section(section))

        lines.append(f"\n*Всего ошибок {self.collector.collector_threshold_label()}: {self.collector.total()}*")
        return "\n".join(lines)

    def build_ok_message(self) -> str:
        """Короткое сообщение когда всё чисто — без перечисления разделов."""
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        return (
            f"✅ *{self.site_name} — Мониторинг {timestamp}*\n..."
            f"Ошибок {self.collector.collector_threshold_label()} не обнаружено.\n"
            f"Проверено разделов: {len(self.SECTIONS)}"
        )

    def has_errors(self) -> bool:
        return self.collector.total() > 0
