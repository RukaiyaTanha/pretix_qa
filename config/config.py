import os

BASE_URL = "http://127.0.0.1:8000"

ORGANIZER_SLUG = "qatesting"
EVENT_SLUG = "qa"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

DEFAULT_TIMEOUT = 10

LOGIN_URL = f"{BASE_URL}/control/login"
EVENT_URL = f"{BASE_URL}/control/event/{ORGANIZER_SLUG}/{EVENT_SLUG}/"