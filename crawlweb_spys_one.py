def spys_one(minimized: bool = False, hideBrowser: bool = False) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver import Chrome as Browser
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

    SERVICE_NAME = "Spys.one:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        ("all", "https://spys.one/en/"),
    ]

    options = Options()
    options.headless = hideBrowser
    options.add_argument("--window-position=0,500")
    options.add_argument("--window-size=1200,500")

    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = Browser(
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

        # GET ANM + HIA RU PROXIES -> PROCEED TO PAGE
        try:
            country_select = driver.find_element(
                by=By.XPATH, value='//select[@id="tldc"]'
            )
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
        except Exception:
            print(SERVICE_NAME, "Home page changed, can't proceed.")
            return None

        # IF AD POPUP SHOWS -> CLOSE
        try:
            close_ad = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located((By.ID, "dismiss-button"))
            )
            actions = ActionChains(driver)
            actions.move_to_element(close_ad)
            actions.click(close_ad)
            actions.perform()
            sleep(3)
        except Exception:
            pass

        # PARCE WHAT YOU GET
        try:
            table_proxy = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table[2]/tbody/tr[4]/td/table/tbody/tr[4]")
                )
            )
        except Exception:
            print(SERVICE_NAME, "Page changed, data not found on page.")
            return None

        try:
            rows_count = len(
                driver.find_elements(
                    by=By.XPATH, value="//table[2]/tbody/tr[4]/td/table/tbody/tr"
                )
            )
            if rows_count == 0:
                # print(SERVICE_NAME, "Page changed, data not found on page.")
                break
        except Exception:
            break

        for row_num in range(3, rows_count - 1):
            try:
                ip_port = driver.find_element(
                    by=By.XPATH,
                    value="//table[2]/tbody/tr[4]/td/table/tbody/tr["
                    + str(row_num + 1)
                    + "]/td[1]",
                )
                protocol = driver.find_element(
                    by=By.XPATH,
                    value="//table[2]/tbody/tr[4]/td/table/tbody/tr["
                    + str(row_num + 1)
                    + "]/td[2]",
                )
                export_proxies.add(
                    protocol.text.split()[0].lower() + "://" + ip_port.text
                )
            except Exception:
                continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(spys_one())
