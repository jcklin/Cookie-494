from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

try:
    # Open a website
    driver.get("https://www.polleverywhere.com")
    cookies = driver.get_cookies()
    for cookie in driver.get_cookies():
        print(f"{cookie['name']} = {cookie['value']}")
    input("Press ENTER to close the browser...")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()