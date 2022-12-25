def proxydocker_com(
    minimized: bool = False,
    hideBrowser: bool = True,
    country_name: str = "Russia",
) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
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

    SERVICE_NAME = "Proxydocker.com:"
    TMOUT = 20
    export_proxies = set()

    urls = [  # pages
        (
            "all",
            "https://www.proxydocker.com/en/proxylist/country/"
            + country_name.capitalize(),
        ),
    ]

    options = Options()
    options.headless = hideBrowser
    options.add_argument("--window-size=1400,900")
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
            return export_proxies

        # PAGING LOOP
        while True:
            try:
                ready = WebDriverWait(driver, TMOUT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except Exception:
                # print(SERVICE_NAME, "Timeout connect to a page", url)
                return export_proxies

            try:
                rows_count = len(
                    driver.find_elements(
                        by=By.XPATH, value='//div[@id="proxylist"]/table/tbody/tr'
                    )
                )
                if rows_count == 0:
                    # print(SERVICE_NAME, "Page changed, data not found on page.")
                    break
            except Exception:
                break

            for row_num in range(rows_count):
                try:
                    ip_port = driver.find_element(
                        by=By.XPATH,
                        value='//div[@id="proxylist"]/table/tbody/tr['
                        + str(row_num + 1)
                        + "]/td[1]",
                    )
                    protocol = driver.find_element(
                        by=By.XPATH,
                        value='//div[@id="proxylist"]/table/tbody/tr['
                        + str(row_num + 1)
                        + "]/td[2]",
                    )
                    export_proxies.add(protocol.text.lower() + "://" + ip_port.text)
                except Exception:
                    continue

            # PAGING NAVIGATION
            try:
                next_page = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//li[contains(@class, "page-item") and not(contains(@class,"disabled")) and @id="nextbtn"]/a')
                    )
                )
                # PAUSE BETWEEN PAGES, TIME TO LOAD
                sleep(TMOUT / 2)
                actions = ActionChains(driver)
                actions.move_to_element(next_page)
                actions.click(next_page)
                actions.perform()
            except Exception:
                # print(SERVICE_NAME, "Can't move to the next page.")
                break

        # PAUSE BETWEEN URLS
        sleep(TMOUT)

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    pr_list = proxydocker_com(
        minimized=False,
        hideBrowser=False,
        country_name="Israel",
    )
    for pr in pr_list:
        print(pr)
