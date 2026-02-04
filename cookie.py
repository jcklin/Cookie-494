from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

a_driver = webdriver.Chrome()
d_driver = webdriver.Chrome()

try:
    # -----------------------------
    # Accept
    # -----------------------------

    # Open the website
    a_driver.get("https://www.polleverywhere.com")

    # Collect cookies before clicking Accept
    print("\nCookies BEFORE clicking Accept:")
    cookies = a_driver.get_cookies()
    for cookie in cookies:
        print(f"{cookie['name']} = {cookie['value']}")

    # Wait until the Accept button is clickable
    wait = WebDriverWait(a_driver, 15)
    accept_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Accept']")
        )
    )

    # Click the Accept button
    accept_button.click()

    # Reload and wait the cookie become stable
    a_driver.refresh()
    WebDriverWait(a_driver, 5).until(
        lambda d: len(d.get_cookies()) > 5
    )

    # Collect cookies after clicking Accept
    print("\nCookies AFTER clicking Accept:")
    cookies = a_driver.get_cookies()
    for cookie in cookies:
        print(f"{cookie['name']} = {cookie['value']}")

    input("\nPress ENTER to continue to Decline flow...")

    # -----------------------------
    # Decline
    # -----------------------------

    # Open the website
    d_driver.get("https://www.polleverywhere.com")

    # Collect cookies before clicking Accept
    print("\nCookies BEFORE clicking Decline:")
    cookies = d_driver.get_cookies()
    for cookie in cookies:
        print(f"{cookie['name']} = {cookie['value']}")

    # Wait until the Accept button is clickable
    wait = WebDriverWait(d_driver, 15)
    decline_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Decline']")
        )
    )

    # Click the Accept button
    decline_button.click()

    # Reload and wait the cookie become stable
    d_driver.refresh()
    WebDriverWait(d_driver, 5).until(
        lambda d: len(d.get_cookies()) > 5
    )

    # Collect cookies after clicking Accept
    print("\nCookies AFTER clicking Decline:")
    cookies = d_driver.get_cookies()
    for cookie in cookies:
        print(f"{cookie['name']} = {cookie['value']}")

    input("\nPress ENTER to close the browser...")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    a_driver.quit()
    d_driver.quit()