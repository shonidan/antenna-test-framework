import time
import pytest
from pages.home_page import HomePage

@pytest.mark.unit
def test_bottom_buttons(driver, screenshot):
    time.sleep(3)
    homepage = HomePage(driver)
    homepage.go_to_subscription()
    screenshot("subscription_page")
    homepage.go_to_inbox()
    screenshot("inbox_page")
    homepage.go_to_queue()
    screenshot("queue_page")
    home_page_text = homepage.go_to_home()
    screenshot("home_page")
    assert "Inicio" in home_page_text.text
    driver.quit()

@pytest.mark.integration
def test_search_podcast(driver, screenshot):
    homepage = HomePage(driver)
    search_section = homepage.go_to_search_section()
    keyword = "Rock Feed"
    search_section.search_by_text(keyword)
    search_section.tap_search_online()
    time.sleep(2)
    results = search_section.get_results()
    print(f"\nResultados encontrados ({len(results)}):")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']} - {r['author']}")

    matches = [
        r for r in results
        if keyword.lower() in r['title'].lower()
    ]

    assert matches, (
            f"No se encontró '{keyword}'. Resultados disponibles:\n" +
            "\n".join(f"- {r['title']}" for r in results)
    )


