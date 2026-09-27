import os

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")
# Strips any trailing slash to avoid double-slash URL errors
if BACKEND_API_URL.endswith("/"):
    BACKEND_API_URL = BACKEND_API_URL[:-1]

APP_TITLE = "MSME Scheme & Subsidy AI Navigator — Administrative Desk"
DEFAULT_JURISDICTION = "Karnataka"
