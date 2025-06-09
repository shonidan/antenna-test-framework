from appium.webdriver.common.appiumby import AppiumBy

class QueueSection:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = (AppiumBy.ID, "id_campo_buscar")
        self.result_list = (AppiumBy.ID, "id_lista_resultados")

    def enter_search_text(self, text):
        self.driver.find_element(*self.search_input).send_keys(text)

    def get_results(self):
        return self.driver.find_elements(*self.result_list)
