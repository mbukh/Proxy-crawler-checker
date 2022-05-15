def freeproxy_world() -> set:
    from time import sleep
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import logging

    SERVICE_NAME = "Freeproxy.world:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        "https://www.freeproxy.world/?type=&anonymity=&country=RU&speed=&port=&page=1",
        "https://www.freeproxy.world/?type=&anonymity=&country=RU&speed=&port=&page=2",
        "https://www.freeproxy.world/?type=&anonymity=&country=RU&speed=&port=&page=3",
    ]

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
        return None

    for url in urls:
        try:
            driver.set_page_load_timeout(TMOUT)
            driver.get(url)
        except:
            print(SERVICE_NAME, "Can't connect to a page", url)

        try:
            table_proxy = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table[@class='layui-table']")
                )
            )
            rows_count = len(
                driver.find_elements(
                    by=By.XPATH, value="//table[@class='layui-table']/tbody[1]/tr"
                )
            )
        except:
            print(SERVICE_NAME, "Page changed, data not found on page.")
            return None

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
                export_proxies.add(ip.text + ":" + port.text)
            except:
                continue
        sleep(5)

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(freeproxy_world())
