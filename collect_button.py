import csv
import os
import requests
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By

from cookie_keywords import (
    ACCEPT_KEYWORDS,
    REJECT_KEYWORDS,
    SPECIAL_KEYWORDS,
    CUSTOMIZE_KEYWORDS,
    ACTION_KEYWORDS,
)

WEBSITES = [
    "https://tinycookie.com/",
    # "https://www.polleverywhere.com/",
    "https://www.paypal.com/us/home",
    "https://trustarc.com/",
    "https://www.digitalocean.com/",
    "https://www.adyen.com/",
    "https://www.bt.com/",
    "https://www.vodafone.com/",
    "https://www.hubspot.com/",
]

BUTTON_TEXT_CSV = "button_text.csv"
BUTTON_TEXT_FIELDS = [
  "website",
  "accept_btn",
  "reject_btn",
  "special_btn",
  "customize_btn",
]

# Selectors from EasyList
EASYLIST_URL = (
    "https://raw.githubusercontent.com/easylist/easylist/master/"
    "easylist_cookie/easylist_cookie_general_hide.txt"
)
# Avoid multiple downloads
EASYLIST_CACHE = "easylist_cookie_selectors.txt"

# Implementation for getting buttons in the cookie action keywords.
def get_buttons(website):
  driver = webdriver.Chrome()

  try:
    driver.get(website)

    # Wait for cookie banner buttons to appear
    time.sleep(2)

    # Try to find the cookie banner first
    banner = find_cookie_banner(driver)

    if banner:
      # Search for buttons only INSIDE the cookie banner
      print("Found cookie banner via EasyList!")
      buttons = banner.find_elements(By.TAG_NAME, "button")
    else:
      # Search for all of the buttons on the page (fallback)
      print("No cookie banner found via EasyList, falling back to all buttons")
      buttons = driver.find_elements(By.TAG_NAME, "button")

    # Sanity Check
    print(f"Found {len(buttons)} buttons!")

    button_info = []
    for index, button in enumerate(buttons):
      button_text = button.text.strip()
      if banner:
        # Banner found: all buttons inside it are cookie-related
        if button_text:
          button_info.append((index + 1, button_text))
      else:
        # No banner: only display those within cookie action keywords
        if is_cookie_action_text(button_text):
          button_info.append((index + 1, button_text))

    return button_info

  # Keep going if an error occurred
  except Exception as e:
    print(f"An error occurred: {type(e).__name__}: {e}")
    traceback.print_exc()
    return []
  finally:
    driver.quit()

# Implementation for checking whether specific text is in cookie action keywords.
def is_cookie_action_text(text):
  t = text.strip().lower()
  if not t:
    return False
  
  return any(k in t for k in ACTION_KEYWORDS)

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

# Get websites URL for websites that are already in the "button_text.csv"
def get_saved_websites(csv_path):
  saved_websites = set()
  if not os.path.exists(csv_path):
    return saved_websites

  file = open(csv_path, "r", newline="", encoding="utf-8")
  try:
    reader = csv.DictReader(file)
    for row in reader:
      website = row.get("website", "").strip()
      if website:
        saved_websites.add(website)
  finally:
    file.close()

  return saved_websites

# Main
if __name__ == "__main__":
  saved_websites = get_saved_websites(BUTTON_TEXT_CSV)
  write_header = not os.path.exists(BUTTON_TEXT_CSV) or os.path.getsize(BUTTON_TEXT_CSV) == 0

  # Loop through the list of websites and add new rows to the CSV file
  for website in WEBSITES:

    # Get the buttons and just dump to console
    print(f"\n{'='*50}")
    print(f"Processing: {website}")
    print(f"{'='*50}")

    # Skip websites that are already in "button_text.csv"
    if website in saved_websites:
      print(f"Skip already saved website.")
      continue

    # Get buttons.
    buttons = get_buttons(website)
    print(f"Cookie buttons found: {buttons}")

    # Sort buttons into different category.
    accept_btn = reject_btn = special_btn = customize_btn = None
    for _, text in buttons:
      lower = text.strip().lower()

      # Priority matters:
      # special > reject > customize > accept
      if special_btn is None and any(k in lower for k in SPECIAL_KEYWORDS):
        special_btn = text
        continue

      if reject_btn is None and any(k in lower for k in REJECT_KEYWORDS):
        reject_btn = text
        continue

      if customize_btn is None and any(k in lower for k in CUSTOMIZE_KEYWORDS):
        customize_btn = text
        continue

      if accept_btn is None and any(k in lower for k in ACCEPT_KEYWORDS):
        accept_btn = text

    # Get button text.
    print(f"Accept button: {accept_btn}")
    print(f"Reject button: {reject_btn}")
    print(f"Special button: {special_btn}")
    print(f"Customize button: {customize_btn}")

    # Save button text to CSV file
    file = open(BUTTON_TEXT_CSV, "a", newline="", encoding="utf-8")
    try:
      writer = csv.DictWriter(
        file,
        fieldnames=BUTTON_TEXT_FIELDS,
      )
      if write_header:
        writer.writeheader()
        write_header = False

      writer.writerow(
        {
          "website": website,
          "accept_btn": accept_btn or "",
          "reject_btn": reject_btn or "",
          "special_btn": special_btn or "",
          "customize_btn": customize_btn or "",
        }
      )
      saved_websites.add(website)
    finally:
      file.close()
