import os
from dotenv import load_dotenv

# .env нужен только для локального запуска.
# В GitHub Actions креды берутся из secrets (env: TG_TOKEN / TG_CHAT_ID в workflow).
load_dotenv(override=False)

# ── Telegram ────────────────────────────────────────────────────────────────
TG_TOKEN   = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

# ── Приложение ───────────────────────────────────────────────────────────────
SITES = [
    {
        "name":     "Elibrium",
        "url":      os.getenv("ELIBRIUM_URL",      "https://app.elibrium.io/auth/login"), #https://app.elibrium.io/auth/login
        "email":    os.getenv("ELIBRIUM_EMAIL",    "mementotot+admin@gmail.com"),
        "password": os.getenv("ELIBRIUM_PASSWORD", ""),
    },
    {
        "name":     "Axiona",
        "url":      os.getenv("AXIONA_URL",      "https://app.axiona.io/auth/login"), #https://app.axiona.io/auth/login
        "email":    os.getenv("AXIONA_EMAIL",    ""), #qa+k+axiona.admin@elibrium.io
        "password": os.getenv("AXIONA_PASSWORD", ""),
    },
]
# BASE_URL = "https://app.elibrium.io/auth/login" #https://app.elibrium.io/auth/login https://app.axiona.io/auth/login

# CREDENTIALS = {
#     "email":    os.getenv("APP_EMAIL",    ""), #qa+k+brandE@elibrium.io
#     "password": os.getenv("APP_PASSWORD", ""),   # локально — из .env, в CI — из secrets
# }

# ── Браузер ──────────────────────────────────────────────────────────────────
VIEWPORT    = {"width": 1280, "height": 700}
SLOW_MO_MS  = 300

# ── Координаты (относительные — пересчитываются под реальный viewport) ───────
# Все значения заданы для базового разрешения 1280×700.
# BrowserManager.scale_coords() автоматически пересчитает их
# если реальный viewport отличается.
BASE_W = 1280
BASE_H = 700

COORDS = {
    "login_email":    (880, 285),
    #"login_password": (880, 380),
    "login_submit":   (880, 490),
    "sidebar": {
        "accounts":        (150, 210),
        "cards":           (150, 270),
        "payments":        (150, 350),
        "refunds":         (150, 400),
        "top_ups":         (150, 320),
        "balance_summary": (150, 400),
    },
    "header": {
        "make_a_deposit": (1140, 160),
        "close":          (1200, 40),
        "card_credentials":(925,495)
    },
    # Табы внутри страниц
    "accounts_tabs": [
        (650, 50),   # первый таб
        (850, 50),   # второй таб
    ],
    "cards_tab":     (1050, 50),
    "show_card":     (500, 340),
}

# ── Какие HTTP-статусы считать ошибками ──────────────────────────────────────
# 300+ — для отладки (чтобы убедиться, что перехват работает)
# Для продакшн-мониторинга поставь 400
ERROR_STATUS_THRESHOLD = 400

IGNORE_URL_PATTERNS = [
    "assets/images/flag",   # битые флаги стран — известная проблема
]
