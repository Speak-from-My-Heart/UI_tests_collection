"""
TelegramNotifier — отправляет текст и фото в Telegram.

Ничего не отправляет, если TG_TOKEN или TG_CHAT_ID не заданы
(удобно для локального запуска без уведомлений).
"""

import time
import requests
from config.settings import TG_TOKEN, TG_CHAT_ID


class TelegramNotifier:
    def __init__(self):
        self._enabled = bool(TG_TOKEN and TG_CHAT_ID)
        if not self._enabled:
            print("TG_TOKEN или TG_CHAT_ID не заданы → уведомления отключены")

    # ── Публичный API ────────────────────────────────────────────────────────

    def send_text(self, text: str) -> None:
        if not self._enabled:
            return
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        payload = {
            "chat_id":    TG_CHAT_ID,
            "text":       text,
            "parse_mode": "Markdown",
        }
        self._post(url, json=payload)

    def send_photo(self, photo_bytes: bytes, caption: str = "") -> None:
        if not self._enabled:
            return
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
        files = {"photo": ("screenshot.png", photo_bytes, "image/png")}
        data  = {"chat_id": TG_CHAT_ID}
        if caption:
            data["caption"]    = caption
            data["parse_mode"] = "Markdown"
        self._post(url, files=files, data=data)

    def send_report_with_screenshots(
        self,
        report_text: str,
        screenshots: list[tuple[str, bytes]],
    ) -> None:
        """
        Отправляет отчёт и скриншоты ТОЛЬКО если есть ошибки.
        screenshots — список пар (название, png_bytes).
        Вызывай этот метод всегда; он сам решит, слать или нет.
        """
        # Проверяем: есть ли в отчёте что-то кроме "всё ок"
        # Логика "слать или нет" лежит в monitor.py — туда передаётся has_errors.
        # Этот метод просто отправляет.
        self.send_text(report_text)
        for name, png_bytes in screenshots:
            self.send_photo(png_bytes, f"Скриншот: *{name}*")
            time.sleep(1.2)   # пауза чтобы Telegram не ругался на flood

    # ── Внутреннее ──────────────────────────────────────────────────────────

    def _post(self, url: str, **kwargs) -> None:
        try:
            r = requests.post(url, timeout=15, **kwargs)
            r.raise_for_status()
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")
