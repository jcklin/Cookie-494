import csv
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# We can try more website.
WEBSITE = "https://www.polleverywhere.com"
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
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Implementation for clicking button.
def clicking_button(website, action):
    driver = webdriver.Chrome()
    try:
        driver.get(website)
        # Wait until the Accept is clickable
        # and decide which button to use.
        wait = WebDriverWait(driver, 15)
        if action.lower() == "accept":
            # This code only work on the button "Accept" and "Decline".
            button_path = "//button[contains(normalize-space(), 'Accept')]"
        elif action.lower() == "decline":
            button_path = "//button[contains(normalize-space(), 'Decline')]"
        else:
            raise ValueError("action must be 'accept' or 'decline'")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_path)))
        # Click the Accept/Decline button.
        button.click()
        # Get cookie after reloading.
        driver.refresh()
        WebDriverWait(driver, 5).until(lambda d: len(d.get_cookies()) > 5)
        return GetCookie(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def get_buttons(website):
    driver = webdriver.Chrome()

    try:
        driver.get(website)

        # Wait for cookie banner buttons to appear
        wait = WebDriverWait(driver, 15)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(), 'Accept')]")))

        # Search for all of the buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")

        # Sanity Check
        print(f"Found {len(buttons)} buttons!")
        print(f"Only displaying those with non-empty button text")

        button_info = []
        for index, button in enumerate(buttons):
            button_text = button.text
            if button_text != '':
                button_info.append((index + 1, button_text))

        return button_info
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    # Get the buttons and just dump to console
    buttons = get_buttons(WEBSITE)
    print(buttons)
    # Get three lists with cookies of this website.
    cookies_before_choice = before_choice(WEBSITE)
    cookies_after_accept = clicking_button(WEBSITE, "accept")
    cookies_after_reject = clicking_button(WEBSITE, "decline")

    # Write in CSV file!
    file = open(OUT_CSV, "w", newline="", encoding="utf-8")
    try:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "website",
                "Before_choice",
                "Accept",
                "Reject",
            ],
        )
        writer.writeheader()

        # Write the Before Choice cookie into CSV.
        for cookie in cookies_before_choice:
            writer.writerow(
                {
                    "website": WEBSITE,
                    "Before_choice": json.dumps(cookie, ensure_ascii=False),
                    "Accept": "",
                    "Reject": "",
                }
            )

        # Write the Accept cookie into CSV.
        for cookie in cookies_after_accept:
            writer.writerow(
                {
                    "website": WEBSITE,
                    "Before_choice": "",
                    "Accept": json.dumps(cookie, ensure_ascii=False),
                    "Reject": "",
                }
            )

        # Write the Reject cookie into CSV.
        for cookie in cookies_after_reject:
            writer.writerow(
                {
                    "website": WEBSITE,
                    "Before_choice": "",
                    "Accept": "",
                    "Reject": json.dumps(cookie, ensure_ascii=False),
                }
            )
    finally:
        file.close()

    print(f"Saved cookie data to {OUT_CSV}")
