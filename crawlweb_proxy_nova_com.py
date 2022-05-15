def proxy_nova_com() -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import logging

    SERVICE_NAME = "Proxynova.com:"
    TMOUT = 20
    export_proxies = set()

    url = "https://www.proxynova.com/proxy-server-list/country-ru/"

    options = Options()
    options.headless = True
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

    try:
        driver.set_page_load_timeout(TMOUT)
        driver.get(url)
    except:
        print(SERVICE_NAME, "Can't connect to a page ", url)
        return None

    try:
        table_proxy = WebDriverWait(driver, TMOUT).until(
            EC.presence_of_element_located((By.ID, "tbl_proxy_list"))
        )
    except:
        print(SERVICE_NAME, "Page changed, data not found on page.")
        return None

    rows_count = len(
        driver.find_elements(
            by=By.XPATH, value='//table[@id="tbl_proxy_list"]/tbody[1]/tr'
        )
    )
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
        except:
            continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(proxy_nova_com())
