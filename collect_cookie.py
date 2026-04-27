import csv
import time
import traceback

from cookie_keywords import ACTION_KEYWORDS
from collect_button import find_cookie_banner

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
  ElementClickInterceptedException,
  JavascriptException,
  StaleElementReferenceException,
  TimeoutException,
)

OUT_CSV = "cookies_result.csv"

# Normalize button text.
def normalize_text(text):
  return " ".join(str(text).strip().lower().split())

# Help to find correct buttons via all the buttons in the web page.
def find_matching_button(driver, button_text):
  target_text = normalize_text(button_text)
  banner = find_cookie_banner(driver)

  candidates = []
  if banner:
    candidates.extend(banner.find_elements(By.TAG_NAME, "button"))
  else:
    candidates.extend(driver.find_elements(By.TAG_NAME, "button"))

  for button in candidates:
    try:
      if normalize_text(button.text) == target_text:
        return button
    except StaleElementReferenceException:
        continue

  for button in candidates:
    try:
      if target_text in normalize_text(button.text):
        return button
    except StaleElementReferenceException:
        continue

  return None

# Adding scrollIntoView to help click buttons.
def scroll_click_button(driver, button):
  driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
    button,
  )
  time.sleep(1)

  try:
    button.click()
    return
  except ElementClickInterceptedException:
    pass

  driver.execute_script("arguments[0].click();", button)

# Get cookies from dirver as list.
def GetCookie(driver):
  cookies = driver.get_cookies()
  result = []
  for c in cookies:
    item = {
      "name": c.get("name", ""),
      "value": c.get("value", "")
    }
    result.append(item)
  return result

# Implementation for writing cookies to csv.
def write_cookies_to_csv(
  out_csv,
  website,
  cookies_before_choice,
  cookies_after_accept,
  cookies_after_reject,
  cookies_after_special,
  accept_button_text,
  reject_button_text,
  special_button_text,
  write_header,
):
  mode ="w" if write_header else "a"
  file = open(out_csv, mode, newline="", encoding="utf-8")
  try:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "website",
            "cookie_name",
            "cookie_value",
            "cookie_count",
            "stage",
            "button_text",
        ],
    )
    if write_header:
      writer.writeheader()

    def write_stage(cookies, stage, button_text):
      cookie_count = len(cookies)

      # Write a row even if there is no Cookie.
      if not cookies:
        writer.writerow(
          {
            "website": website,
            "cookie_name": "",
            "cookie_value": "",
            "cookie_count": cookie_count,
            "stage": stage,
            "button_text": button_text,
          }
        )
        return
      
      # Normal writing
      for cookie in (cookies):
        writer.writerow(
          {
            "website": website,
            "cookie_name": cookie.get("name", ""),
            "cookie_value": cookie.get("value", ""),
            "cookie_count": cookie_count,
            "stage": stage,
            "button_text": button_text,
          }
        )

    write_stage(cookies_before_choice, "page_load", "")
    write_stage(cookies_after_accept, "after_accept", accept_button_text)
    write_stage(cookies_after_reject, "after_reject", reject_button_text)
    write_stage(cookies_after_special, "after_special", special_button_text)
  finally:
      file.close()

# Before choice implementation.
def before_choice(website):
  driver = webdriver.Chrome()
  try:
    driver.get(website)
    time.sleep(2)
    return GetCookie(driver)
  except Exception as e:
    print(f"An error occurred: {type(e).__name__}: {e}")
    traceback.print_exc()
    return []
  finally:
    driver.quit()

# Implementation for clicking button.
def clicking_button(website, button_text):
  if button_text is None or not str(button_text).strip():
    print("Skip clicking: button_text is empty.")
    return []
  
  driver = webdriver.Chrome()
  try:
    driver.get(website)
    # Wait until the button is clickable, wait at most 6 seconds.
    wait = WebDriverWait(driver, 6)

    button = wait.until(lambda d: find_matching_button(d, button_text))
    scroll_click_button(driver, button)

    try:
      wait.until(EC.staleness_of(button))
    except (TimeoutException, StaleElementReferenceException):
      time.sleep(2)

    return GetCookie(driver)
  except TimeoutException:
    print(f"TimeoutException: could not click button '{button_text}' within 6 seconds on {website}")
    return []
  except JavascriptException as e:
    print(f"JavascriptException while clicking '{button_text}' on {website}: {e}")
    return []
  except Exception as e:
    print(f"An error occurred: {type(e).__name__}: {e}")
    return []
  finally:
    driver.quit()

if __name__ == "__main__":

  BUTTON_TEXT_CSV = "button_text.csv"
  first_website = True

  file = open(BUTTON_TEXT_CSV, "r", newline="", encoding="utf-8")
  try:
    reader = csv.DictReader(file)
    for row in reader:
      website = row.get("website", "").strip()
      accept_btn = row.get("accept_btn", "").strip()
      reject_btn = row.get("reject_btn", "").strip()
      special_btn = row.get("special_btn", "").strip()

      if not website:
        continue

      # Get page_load cookies.
      cookies_before_choice = before_choice(website)

      # Click the discovered buttons
      cookies_after_accept = clicking_button(website, accept_btn) if accept_btn else []
      cookies_after_reject = clicking_button(website, reject_btn) if reject_btn else []
      cookies_after_special = clicking_button(website, special_btn) if special_btn else []

      # Write in CSV file!
      write_cookies_to_csv(
        OUT_CSV,
        website,
        cookies_before_choice,
        cookies_after_accept,
        cookies_after_reject,
        cookies_after_special,
        accept_btn or "",
        reject_btn or "",
        special_btn or "",
        write_header=first_website,
      )
      first_website = False

      print(f"Saved cookie data to {OUT_CSV} from {website}")
  finally:
    file.close()
