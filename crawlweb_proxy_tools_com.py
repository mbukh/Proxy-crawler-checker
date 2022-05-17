def proxy_tools_com(minimized: bool = False, hideBrowser: bool = False) -> set:
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

    SERVICE_NAME = "Proxy-tools.com:"
    TMOUT = 30
    export_proxies = set()

    urls = [
        ("all", "https://proxy-tools.com/proxy/ru"),
    ]

    options = Options()
    options.headless = hideBrowser
    options.add_argument("--window-position=1200,100")
    options.add_argument("--window-size=1024,768")

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
        except:
            print(SERVICE_NAME, "Timeout connect to a page", url)

            # ADD PAGING !!

        # IF CAPTCHA EXISTS - PASS IT
        MAX_TRIES = 2
        tried = 0
        while True:
            try:
                request_ports = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='ct-main']/main/table/tbody/tr[1]/td[2]/a")
                    )
                )
                actions = ActionChains(driver)
                actions.move_to_element(request_ports)
                actions.click(request_ports)
                actions.perform()
                # WAITING FOR A USER TO PASS CAPTCHA
                sleep(TMOUT)
                if tried >= MAX_TRIES:
                    print(SERVICE_NAME, "Captcha not passed.")
                    return None
                tried += 1
            except:
                break

        try:
            rows_count = len(
                driver.find_elements(
                    by=By.XPATH, value="//div[@id='ct-main']/main/table/tbody/tr"
                )
            )
            if rows_count == 0:
                # print(SERVICE_NAME, "Page changed, data not found on page.")
                break
        except:
            break

        for row_num in range(rows_count):
            try:
                ip = driver.find_element(
                    by=By.XPATH,
                    value="//*[@id='ct-main']/main/table/tbody/tr["
                    + str(row_num + 1)
                    + "]/td[1]",
                )
                port = driver.find_element(
                    by=By.XPATH,
                    value="//*[@id='ct-main']/main/table/tbody/tr["
                    + str(row_num + 1)
                    + "]/td[2]",
                )
                protocol = driver.find_element(
                    by=By.XPATH,
                    value="//*[@id='ct-main']/main/table/tbody/tr["
                    + str(row_num + 1)
                    + "]/td[3]",
                )
                export_proxies.add(
                    protocol.text.lower() + "://" + ip.text + ":" + port.text
                )
            except:
                continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(proxy_tools_com())
