def proxydb_net(minimized: bool = False, hideBrowser: bool = False) -> set:
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
    import os

    # Turn off webdriver-manager logs
    os.environ["WDM_LOG"] = str(logging.NOTSET)
    # By default, all driver binaries are saved to user.home/.wdm folder.
    # You can override this setting and save binaries to project.root/.wdm.
    os.environ["WDM_LOCAL"] = "1"

    SERVICE_NAME = "Proxydb.net:"
    TMOUT = 30
    export_proxies = set()

    urls = [
        (
            "all",
            "https://proxydb.net/?protocol=https&protocol=socks4&protocol=socks5&anonlvl=2&anonlvl=3&anonlvl=4&country=RU",
        ),
    ]

    options = Options()
    options.headless = hideBrowser
    options.add_argument("--window-position=0,100")
    options.add_argument("--window-size=1024,768")

    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(path="./chromedriver").install(),
            ),
            options=options,
        )
    except Exception as e:
        print(SERVICE_NAME, "Can't open browser driver.")
        print(e)
        return None

    if minimized:
        driver.minimize_window()  # if no user interaction needed, but browser must be open

    for proxy_type, url in urls:
        try:
            # EXPLICIT WAIT
            w = WebDriverWait(driver, TMOUT)
            # LAUNCH URL
            driver.get(url)
            # EXPECTED CONDITION
            w.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # JAVASCRIPT EXECUTOR TO STOP PAGE LOAD
            driver.execute_script("window.stop();")
        except Exception:
            print(SERVICE_NAME, "Timeout connect to a page", url)

        while True:
            try:
                rows_count = len(
                    driver.find_elements(by=By.XPATH, value="//div/div/table/tbody/tr")
                )
                if rows_count == 0:
                    # print(SERVICE_NAME, "Page changed, data not found on page.")
                    break
            except Exception:
                break

            oldLen = len(export_proxies)

            for row_num in range(rows_count):
                try:
                    ip_port = driver.find_element(
                        by=By.XPATH,
                        value="//div/div/table/tbody/tr["
                        + str(row_num + 1)
                        + "]/td[1]",
                    )
                    protocol = driver.find_element(
                        by=By.XPATH,
                        value="//div/div/table/tbody/tr["
                        + str(row_num + 1)
                        + "]/td[5]",
                    )
                    export_proxies.add(protocol.text.lower() + "://" + ip_port.text)
                except Exception:
                    continue

            # new page not detected ( new proxies ) -> driver.quit()
            if len(export_proxies) == oldLen:
                # print(SERVICE_NAME, "Captcha not passed.")
                break

            # PAGING NAVIGATION
            try:
                next_page = WebDriverWait(driver, TMOUT).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='paging-form']/nav/ul/button")
                    )
                )
                # SCROLL DOWN A PAGE AND MOUSE CLICKS
                driver.execute_script(
                    "var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;"
                )
                sleep(1)
                actions = ActionChains(driver)
                actions.move_to_element(next_page)
                actions.click(next_page)
                actions.perform()
            except Exception:
                # print(SERVICE_NAME, "Can't move to the next page.")
                break

            # WAIT FOR CAPTCHA PASS
            sleep(TMOUT)

            # WAIT FOR RELOAD
            try:
                table_proxies = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div/div/table/tbody/tr")
                    )
                )
            except Exception:
                continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(proxydb_net())
