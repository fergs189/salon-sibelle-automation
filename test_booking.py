import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

path = Path(__file__).resolve().parent / "data" / "single_services.csv"
with path.open(newline="", encoding="utf-8-sig") as file:
    services = list(csv.DictReader(file))

SERVICE = (By.CSS_SELECTOR, 'input[placeholder="Select Service"]')
SEARCH = (By.XPATH, '//a[normalize-space()="Show Available Times"]')
ERROR = (By.ID, "serviceRequiredError")
RESULTS = (
    By.XPATH,
    '//h2[normalize-space()="When Should Your Appointment Start?"]'
)
TIMES = (
    By.CSS_SELECTOR,
    'a[onclick*="AvailableTimeSelected_TimeStep"]'
)


def open_booking():
    driver = webdriver.Chrome()
    wait = WebDriverWait(
        driver, 40,
        ignored_exceptions=(StaleElementReferenceException,)
    )

    try:
        driver.get("https://www.salonsibelle.ca/")
        old_tabs = set(driver.window_handles)

        wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Book Online"))
        ).click()

        wait.until(
            lambda d: bool(set(d.window_handles) - old_tabs)
            or "mysalononline.com" in d.current_url
        )

        new_tabs = set(driver.window_handles) - old_tabs
        if new_tabs:
            driver.switch_to.window(next(iter(new_tabs)))

        wait.until(EC.visibility_of_element_located(SERVICE))
        wait.until(
            lambda d: d.find_element(*SERVICE).get_attribute("value") == ""
        )
        return driver, wait

    except Exception:
        driver.quit()
        raise


def select_service(driver, wait, name):
    field = wait.until(EC.element_to_be_clickable(SERVICE))
    field.clear()
    field.send_keys(name)

    def click_option(browser):
        for option in browser.find_elements(By.CSS_SELECTOR, "li"):
            if option.is_displayed() and option.text.strip() == name:
                option.click()
                return True
        return False

    wait.until(click_option)
    wait.until(
        lambda d: d.find_element(*SERVICE).get_attribute("value") == name
    )


def check_empty_service(driver, wait):
    assert driver.find_element(*SERVICE).get_attribute("value") == ""

    wait.until(EC.element_to_be_clickable(SEARCH)).click()

    error = wait.until(EC.visibility_of_element_located(ERROR))
    assert error.text.strip() == "Select a service"


for flow in [1, 2]:
    for row in services:
        driver, wait = open_booking()

        try:
            if flow == 2:
                check_empty_service(driver, wait)

            name = row["service"]
            select_service(driver, wait, name)

            assert (
                driver.find_element(*SERVICE).get_attribute("value") == name
            )

            wait.until(EC.element_to_be_clickable(SEARCH)).click()

            assert wait.until(
                EC.visibility_of_element_located(RESULTS)
            ).is_displayed()

            times = wait.until(
                lambda d: [
                    item.text.strip()
                    for item in d.find_elements(*TIMES)
                    if item.is_displayed() and item.text.strip()
                ]
            )
            assert len(times) > 0

        finally:
            driver.quit()

    if flow == 1:
        driver, wait = open_booking()
        try:
            check_empty_service(driver, wait)
        finally:
            driver.quit()
