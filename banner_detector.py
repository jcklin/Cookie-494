import os
import requests
from selenium.webdriver.common.by import By

# Selectors from EasyList
EASYLIST_URL = (
    "https://raw.githubusercontent.com/easylist/easylist/master/"
    "easylist_cookie/easylist_cookie_general_hide.txt"
)
# Avoid multiple downloads
EASYLIST_CACHE = "easylist_cookie_selectors.txt"

# Download CSS
def download_easylist(url=EASYLIST_URL, cache_path=EASYLIST_CACHE):
    """Download EasyList cookie selectors and cache locally."""
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if len(lines) > 10:
            return lines

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return resp.text.splitlines()


def parse_easylist_selectors(lines):
    """
    Parse EasyList lines into CSS selectors.

    Lines with text BEFORE ## are domain-specific — we skip those.
    Lines starting with ! are comments.
    """
    selectors = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        if "##" in line:
            parts = line.split("##", 1)
            # Skip if domain specific
            if parts[0].strip():
                continue
            # get the selector
            selector = parts[1].strip()
            if selector:
                selectors.append(selector)
    return selectors


def get_cookie_banner_selectors():
    """Return list of CSS selectors for known cookie banners."""
    lines = download_easylist()
    return parse_easylist_selectors(lines)


def find_cookie_banner(driver, selectors=None):
    """
    Try each EasyList selector until we find a visible cookie banner.
    Returns the WebElement if found, None otherwise.
    """
    if selectors is None:
        selectors = get_cookie_banner_selectors()

    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                if el.is_displayed():
                    return el
        except Exception:
            continue
    return None