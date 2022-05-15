def spys_one(minimized: bool = False, showBrowser: bool = True) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.action_chains import ActionChains
    from time import sleep
    import logging

    SERVICE_NAME = "Spys.one:"
    TMOUT = 30
    export_proxies = set()

    url = "https://spys.one/en/"

    options = Options()
    options.headless = not showBrowser
    options.add_argument("--window-size=1024,400")
    options.add_argument("--window-position=500,500")
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
        print(SERVICE_NAME, "Can't connect to a page ", url)
        return None

    # get ANM + HIA RU proxies -> proceed to page
    try:
        show_more = WebDriverWait(driver, TMOUT).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[3]/td/table",
                )
            )
        )
        country_select = driver.find_element(by=By.XPATH, value='//select[@id="tldc"]')
        country_select = Select(country_select)
        country_select.select_by_value("191")  # Russia
        sleep(1)
        anon_select = driver.find_element(by=By.XPATH, value='//select[@id="anmm"]')
        anon_select = Select(anon_select)
        anon_select.select_by_value("1")  # ANM + HIA
        sleep(2)
        submit_input = driver.find_element(
            by=By.XPATH,
            value='//input[contains(@class,"spy8") and contains(@type,"submit")]',
        )
        submit_input.click()
        sleep(3)
    except:
        print(SERVICE_NAME, "Home page changed, can't proceed.")
        return None

    # if ad popup shows -> close
    try:
        close_ad = WebDriverWait(driver, TMOUT).until(
            EC.presence_of_element_located((By.ID, "dismiss-button"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(close_ad)
        actions.click(close_ad)
        actions.perform()
        sleep(3)
    except:
        pass

    # parce what you get
    try:
        table_proxy = WebDriverWait(driver, TMOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//table[2]/tbody/tr[4]/td/table/tbody/tr[4]")
            )
        )
        rows_count = len(
            driver.find_elements(
                by=By.XPATH, value="//table[2]/tbody/tr[4]/td/table/tbody/tr"
            )
        )
    except:
        print(SERVICE_NAME, "Page changed, data not found on page.")
        return None

    for row_num in range(3, rows_count - 1):
        try:
            ip_port = driver.find_element(
                by=By.XPATH,
                value="//table[2]/tbody/tr[4]/td/table/tbody/tr["
                + str(row_num + 1)
                + "]/td[1]",
            )
            export_proxies.add(ip_port.text)
        except:
            continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(spys_one())
