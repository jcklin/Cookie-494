import csv
import time

from cookie_keywords import ACTION_KEYWORDS
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

        # Search for all of the buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")

        # Sanity Check
        print(f"Found {len(buttons)} buttons!")
        print(f"Only displaying those within cookie action keywords")

        button_info = []
        for index, button in enumerate(buttons):
            button_text = button.text
            if is_cookie_action_text(button_text):
                button_info.append((index + 1, button_text))

        return button_info
    except Exception as e:
        print(f"An error occurred: {e}")
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
):
    file = open(out_csv, "w", newline="", encoding="utf-8")
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

if __name__ == "__main__":
    # Get the buttons and just dump to console
    buttons = get_buttons(WEBSITE)
    print(buttons)
    
    # Get three lists with cookies of this website.
    cookies_before_choice = before_choice(WEBSITE)
    cookies_after_accept = clicking_button(WEBSITE, "accept")
    cookies_after_reject = clicking_button(WEBSITE, "decline")

    # Get button text.
    accept_button_text = "Accept"
    reject_button_text = "Decline"

    # Write in CSV file!
    write_cookies_to_csv(
        OUT_CSV,
        WEBSITE,
        cookies_before_choice,
        cookies_after_accept,
        cookies_after_reject,
        accept_button_text,
        reject_button_text,
    )

    print(f"Saved cookie data to {OUT_CSV}")
