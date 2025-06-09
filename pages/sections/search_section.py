from appium.webdriver.common.appiumby import AppiumBy
from pages.wait_utils import wait_for_text, wait_for_xpath

class SearchSection:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.search_input = (AppiumBy.ID, "de.danoeh.antennapod:id/search_src_text")
        self.click_search_online = (AppiumBy.ID, "de.danoeh.antennapod:id/actionButton")

        self.results_grid = (AppiumBy.XPATH, '//android.widget.GridView[@resource-id="de.danoeh.antennapod:id/gridView"]')
        self.result_title = (AppiumBy.ID, "de.danoeh.antennapod:id/txtvTitle")

    def search_by_text(self, text):
        self.driver.find_element(*self.search_input).send_keys(text)

    def tap_search_online(self):
        wait_for_text(self.driver, "Buscar en línea", self.timeout)
        self.driver.find_element(*self.click_search_online).click()

    def get_results(self):
        """Obtiene todos los resultados con título, autor y elemento"""
        try:
            # Esperar a que cargue al menos un resultado
            wait_for_xpath(
                self.driver,
                '//android.widget.RelativeLayout[.//*[@resource-id="de.danoeh.antennapod:id/txtvTitle"]]',
                self.timeout
            )

            results = []
            items = self.driver.find_elements(
                AppiumBy.XPATH,
                '//android.widget.RelativeLayout[.//*[@resource-id="de.danoeh.antennapod:id/txtvTitle"]]'
            )

            for item in items:
                try:
                    title_el = item.find_element(AppiumBy.ID, "de.danoeh.antennapod:id/txtvTitle")
                    author_el = item.find_element(AppiumBy.ID, "de.danoeh.antennapod:id/txtvAuthor")

                    results.append({
                        'title': title_el.text.strip(),
                        'author': author_el.text.strip(),
                        'element': item
                    })
                except Exception as e:
                    print(f"Error procesando item: {str(e)}")
                    continue

            return results

        except Exception as e:
            print(f"Error en get_results(): {str(e)}")
            return []