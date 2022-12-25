def proxyservers_pro(
    minimized: bool = False,
    hideBrowser: bool = True,
    country_code: str = "ru",
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

    SERVICE_NAME = "Proxyservers.pro:"
    TMOUT = 20
    export_proxies = set()

    urls = [  # pages
        (
            "all",
            "https://proxyservers.pro/proxy/list/country/"
            + country_code.upper()
            + "/order/updated/order_dir/desc/page/1",
        ),
    ]

    options = Options()
    options.headless = hideBrowser
    options.add_argument("--window-position=400,500")
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
            return export_proxies

        # PAGING LOOP
        while True:
            try:
                ready = WebDriverWait(driver, TMOUT).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@class="card-body"]/div/table')
                    )
                )
            except Exception:
                print(SERVICE_NAME, "Timeout connect to a page", url)
                return export_proxies

            try:
                rows_count = len(
                    driver.find_elements(
                        by=By.XPATH,
                        value='//div[@class="card-body"]/div/table/tbody/tr[@valign="top"]',
                    )
                )
                if rows_count == 0:
                    # print(SERVICE_NAME, "Page changed, data not found on page.")
                    break
            except Exception:
                break

            for row_num in range(rows_count):
                try:
                    ip = driver.find_element(
                        by=By.XPATH,
                        value='//div[@class="card-body"]/div/table/tbody/tr[@valign="top"]['
                        + str(row_num + 1)
                        + "]/td[2]",
                    )
                    port = driver.find_element(
                        by=By.XPATH,
                        value='//div[@class="card-body"]/div/table/tbody/tr[@valign="top"]['
                        + str(row_num + 1)
                        + "]/td[3]",
                    )
                    export_proxies.add(ip.text + ":" + port.text)
                except Exception:
                    continue

            # PAGING NAVIGATION
            try:
                next_page = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//div[@class='card-footer']/nav/ul/li[@class='page-item active']//following-sibling::li[1]",
                        )
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
    pr_list = proxyservers_pro(
        minimized=False,
        hideBrowser=False,
        country_code="il",
    )
    for pr in pr_list:
        print(pr)
