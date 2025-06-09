from appium.webdriver.common.appiumby import AppiumBy

from pages.sections.queue_section import QueueSection
from pages.sections.search_section import SearchSection
from pages.wait_utils import wait_for_text

class HomePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        
        #Top options
        self.search_button = (AppiumBy.ID, "de.danoeh.antennapod:id/action_search")
        self.options = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Más opciones']")

        #Bottom options
        self.home_page = (AppiumBy.ID, "de.danoeh.antennapod:id/bottom_navigation_home")
        self.queue = (AppiumBy.ID, "de.danoeh.antennapod:id/bottom_navigation_queue")
        self.inbox = (AppiumBy.ID, "de.danoeh.antennapod:id/bottom_navigation_inbox")
        self.subscriptions = (AppiumBy.ID, "de.danoeh.antennapod:id/bottom_navigation_subscriptions")
        self.more_options = (AppiumBy.ID, "de.danoeh.antennapod:id/bottom_navigation_more")

    def go_to_search_section(self):
        self.driver.find_element(*self.search_button).click()
        wait_for_text(self.driver, "Escribe un término de búsqueda", self.timeout)
        return SearchSection(self.driver)

    def go_to_options(self):
        self.driver.find_element(*self.search_button).click()
        return SearchSection(self.driver)

    def go_to_home(self):
        self.driver.find_element(*self.home_page).click()
        home_text = wait_for_text(self.driver, "Inicio", self.timeout)
        return home_text

    def go_to_queue(self):
        self.driver.find_element(*self.queue).click()
        queue_text = wait_for_text(self.driver, "Cola", self.timeout)
        return queue_text, QueueSection(self.driver)

    def go_to_inbox(self):
        self.driver.find_element(*self.inbox).click()
        inbox_text = wait_for_text(self.driver, "Bandeja de entrada", self.timeout)
        return inbox_text, SearchSection(self.driver)

    def go_to_subscription(self):
        self.driver.find_element(*self.subscriptions).click()
        subscription_text = wait_for_text(self.driver, "Suscripciones", self.timeout)
        return subscription_text, SearchSection(self.driver)

    def go_to_more_options(self):
        self.driver.find_element(*self.more_options).click()
        return SearchSection(self.driver)