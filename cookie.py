import csv
import time
import traceback

from cookie_keywords import ACTION_KEYWORDS
from banner_detector import find_cookie_banner
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# We can try more website.
WEBSITE = "https://www.polleverywhere.com"

WEBSITES = [
    "https://tinycookie.com/",
    "https://www.polleverywhere.com",
    "https://www.ferrari.com/en-US",
    "https://www.t-mobile.com/switch/new-customer-switch-deals?gclsrc=aw.ds&&cmpid=MGPO_PB_P_EVGRNPSTPD_26741626_135032613545_778421130718&gad_source=1&gad_campaignid=16905361619&gbraid=0AAAAAD79WuVp3FzMfqdMwPJ_7FaAIPxY1&gclid=CjwKCAiAmp3LBhAkEiwAJM2JUP4kDZK9CcD0UuQ8YGlNcofSRuqkLDt2TNpbyPnjkFGd4uEVF-h_khoCNucQAvD_BwE",
]

OUT_CSV = "cookies_result.csv"

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
    driver = webdriver.Chrome()
    try:
        driver.get(website)
        # Wait until the button is clickable
        wait = WebDriverWait(driver, 15)
        # Match any button containing the target text, should work on more buttons now
        button_path = f"//button[contains(normalize-space(), '{button_text}')]"
        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_path)))
        # Click the button
        button.click()
        # Get cookie after reloading
        driver.refresh()
        # Wait for page to load
        time.sleep(3)
        return GetCookie(driver)
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

# Implementation for writing cookies to csv.
def write_cookies_to_csv(
    out_csv,
    website,
    cookies_before_choice,
    cookies_after_accept,
    cookies_after_reject,
    accept_button_text,
    reject_button_text,
    write_header=True,
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
                "stage",
                "button_text",
            ],
        )
        if write_header:
            writer.writeheader()

        def write_stage(cookies, stage, button_text):
            for cookie in (cookies):
                writer.writerow(
                    {
                        "website": website,
                        "cookie_name": cookie.get("name", ""),
                        "cookie_value": cookie.get("value", ""),
                        "stage": stage,
                        "button_text": button_text,
                    }
                )

        write_stage(cookies_before_choice, "page_load", "")
        write_stage(cookies_after_accept, "after_accept", accept_button_text)
        write_stage(cookies_after_reject, "after_reject", reject_button_text)
    finally:
        file.close()
