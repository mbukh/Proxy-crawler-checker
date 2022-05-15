def get_proxy_proxydb_net(minimized: bool = False, showBrowser: bool = True) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.action_chains import ActionChains
    from time import sleep
    import logging

    SERVICE_NAME = "Proxydb.net:"
    TMOUT = 30
    export_proxies = set()

    url = "https://proxydb.net/?protocol=https&protocol=socks4&protocol=socks5&anonlvl=2&anonlvl=3&anonlvl=4&country=RU"

    options = Options()
    options.headless = not showBrowser
    options.add_argument("--window-size=1024,768")
    options.add_argument("--window-position=0,100")
    try:
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(
                    log_level=logging.WARNING, print_first_line=False
                ).install()
            ),
            options=options,
        )
    except:
        print(SERVICE_NAME, "Can't connect to the server.")
        return None

    if minimized:
        driver.minimize_window()  # if no user interaction needed, but browser must be open

    try:
        driver.set_page_load_timeout(TMOUT)
        driver.get(url)
    except:
        print("Can't connect to a page ", url)
        return None

    run = True

    while run:
        try:
            table_proxy = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located((By.XPATH, "//div/div/table/tbody/tr"))
            )
            rows_count = len(
                driver.find_elements(by=By.XPATH, value="//div/div/table/tbody/tr")
            )
        except:
            print("Proxydb.net: Page changed, data not found on page.")
            break

        oldLen = len(export_proxies)

        for row_num in range(rows_count):
            try:
                ip_port = driver.find_element(
                    by=By.XPATH,
                    value="//div/div/table/tbody/tr[" + str(row_num + 1) + "]/td[1]",
                )
                export_proxies.add(ip_port.text)
            except:
                continue

        # new page not detected ( new proxies ) -> driver.quit()
        if len(export_proxies) == oldLen:
            break

        try:
            next_page = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='paging-form']/nav/ul/button")
                )
            )
        except:
            print("Proxydb.net: Can't perform next page.")
            break

        # scroll down a page and mouse clicks
        driver.execute_script(
            "var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;"
        )
        sleep(1)
        actions = ActionChains(driver)
        actions.move_to_element(next_page)
        actions.click(next_page)
        actions.perform()
        sleep(10)

        try:
            rows_count = len(
                driver.find_elements(by=By.XPATH, value="//div/div/table/tbody/tr")
            )
        except:
            break

    driver.quit()

    print("Proxydb.net:", len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(get_proxy_proxydb_net())
