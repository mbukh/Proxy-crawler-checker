def proxy_nova_com(minimized: bool = False, hideBrowser: bool = False) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from time import sleep
    import logging

    SERVICE_NAME = "Proxynova.com:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        ("all", "https://www.proxynova.com/proxy-server-list/country-ru/"),
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
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(
                    log_level=logging.WARNING, print_first_line=False
                ).install()
            ),
            options=options,
        )
    except Exception:
        print(SERVICE_NAME, "Can't open browser driver.")
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
                    by=By.XPATH, value='//table[@id="tbl_proxy_list"]/tbody[1]/tr'
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
                    value='//table[@id="tbl_proxy_list"]/tbody[1]/tr['
                    + str(row_num + 1)
                    + "]/td[1]",
                )
                port = driver.find_element(
                    by=By.XPATH,
                    value='//table[@id="tbl_proxy_list"]/tbody[1]/tr['
                    + str(row_num + 1)
                    + "]/td[2]",
                )
                export_proxies.add(ip.text + ":" + port.text)
            except Exception:
                continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(proxy_nova_com())
