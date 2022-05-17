def premproxy_com(minimized: bool = False, hideBrowser: bool = True) -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from time import sleep
    import logging

    SERVICE_NAME = "Premproxy.com:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        ("all", "https://premproxy.com/proxy-by-country/Russian-Federation-01.htm"),
        ("all", "https://premproxy.com/proxy-by-country/Russian-Federation-02.htm"),
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
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(
                    log_level=logging.WARNING, print_first_line=False
                ).install()
            ),
            options=options,
        )
    except:
        print(SERVICE_NAME, "Can't open browser driver.")
        return export_proxies

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
        except:
            print(SERVICE_NAME, "Timeout connect to a page", url)

        rows_count = len(
            driver.find_elements(
                by=By.XPATH, value='//*[@id="proxylist"]/div/table/tbody/tr'
            )
        )
        if rows_count == 0:
            # print(SERVICE_NAME, "Page changed, data not found on page.")
            continue

        for row_num in range(rows_count):
            try:
                ip_port = driver.find_element(
                    by=By.XPATH,
                    value='//*[@id="proxylist"]/div/table/tbody/tr['
                    + str(row_num + 1)
                    + "]/td[1]",
                )
                export_proxies.add(ip_port.text)
            except:
                continue
        sleep(5)

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(premproxy_com())
