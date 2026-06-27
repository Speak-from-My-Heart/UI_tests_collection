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

    def send_text(self, text: str) -> bool:
        if not self._enabled:
            return True
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        ok = True
        for chunk in chunks:
            payload = {"chat_id": TG_CHAT_ID, "text": chunk, "parse_mode": "Markdown"}
            if not self._post(url, json=payload):
                # Markdown сломался (спецсимволы в URL и т.п.) — шлём plain text
                payload.pop("parse_mode")
                if not self._post(url, json=payload):
                    ok = False
        return ok

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

    def send_screenshots_report(
        self,
        site_name: str,
        screenshots: list[tuple[str, bytes]],
    ) -> None:
        self.send_text(f"🖼 *Тестовая выгрузка скринов* — {site_name}")
        for name, png_bytes in screenshots:
            self.send_photo(png_bytes, f"Скриншот: *{name}*")
            time.sleep(1.2)

    def send_report_with_screenshots(
        self,
        report_text: str,
        screenshots: list[tuple[str, bytes]],
    ) -> None:
        self.send_text(report_text)
        for name, png_bytes in screenshots:
            self.send_photo(png_bytes, f"Скриншот: *{name}*")
            time.sleep(1.2)

    # ── Внутреннее ──────────────────────────────────────────────────────────

    def _post(self, url: str, **kwargs) -> bool:
        try:
            r = requests.post(url, timeout=15, **kwargs)
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")
            return False
