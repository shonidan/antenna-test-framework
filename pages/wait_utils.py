from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def wait_for_text(driver, text, timeout=10):
    xpath_expr = f"//*[contains(@text, '{text}')]"
    locator = (AppiumBy.XPATH, xpath_expr)
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_for_button(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_for_id(driver, element_id, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((AppiumBy.ID, element_id))
    )

def wait_for_xpath(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((AppiumBy.XPATH, xpath))
    )