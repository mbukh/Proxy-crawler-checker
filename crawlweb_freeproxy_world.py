def freeproxy_world(minimized: bool = False, hideBrowser: bool = False) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver import Chrome as Browser
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from time import sleep
    import logging
    import os

    # Turn off webdriver-manager logs
    os.environ["WDM_LOG"] = str(logging.NOTSET)
    # By default, all driver binaries are saved to user.home/.wdm folder.
    # You can override this setting and save binaries to project.root/.wdm.
    os.environ["WDM_LOCAL"] = "1"

    SERVICE_NAME = "Freeproxy.world:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        (
            "socks4",
            "https://www.freeproxy.world/?type=socks4&anonymity=&country=RU&speed=&port=&page=1",
        ),
        (
            "socks5",
            "https://www.freeproxy.world/?type=socks5&anonymity=&country=RU&speed=&port=&page=1",
        ),
        (
            "https",
            "https://www.freeproxy.world/?type=https&anonymity=&country=RU&speed=&port=&page=1",
        ),
    ]

    options = Options()
    options.headless = True
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

        try:
            rows_count = len(
                driver.find_elements(
                    by=By.XPATH, value="//table[@class='layui-table']/tbody[1]/tr"
                )
            )
            if rows_count == 0:
                # print(SERVICE_NAME, "Page changed, data not found on page.")
                break
        except Exception:
            break

        for row_num in range(2, rows_count):
            try:
                ip = driver.find_element(
                    by=By.XPATH,
                    value="//table[@class='layui-table']/tbody[1]/tr["
                    + str(row_num + 1)
                    + "]/td[1]",
                )
                port = driver.find_element(
                    by=By.XPATH,
                    value="//table[@class='layui-table']/tbody[1]/tr["
                    + str(row_num + 1)
                    + "]/td[2]",
                )
                protocol = driver.find_element(
                    by=By.XPATH,
                    value="//table[@class='layui-table']/tbody[1]/tr["
                    + str(row_num + 1)
                    + "]/td[6]",
                )
                export_proxies.add(protocol.text + "://" + ip.text + ":" + port.text)
            except Exception:
                continue
        sleep(5)

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(freeproxy_world())
