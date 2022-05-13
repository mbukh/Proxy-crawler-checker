def get_proxy_free_proxy_cz() -> set:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from time import sleep
    import logging

    SERVICE_NAME = "Free-proxy.cz:"
    TMOUT = 20
    export_proxies = set()

    urls = ['http://free-proxy.cz/ru/proxylist/country/RU/https/ping/level1',
            'http://free-proxy.cz/ru/proxylist/country/RU/https/ping/level2',
            'http://free-proxy.cz/ru/proxylist/country/RU/socks/ping/level1', # pages
            'http://free-proxy.cz/ru/proxylist/country/RU/socks/ping/level2',
            ]

    options = Options()
    options.headless = True
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=logging.WARNING, print_first_line=False).install()), options=options)
    except:
        print(SERVICE_NAME, "Can't connect to the server.")
        return None




        # PAGING !!





    for url in urls:
        try:
            driver.set_page_load_timeout(TMOUT)
            driver.get(url)
        except:
            print("Can't connect to a page ", url)
            return None
        
        try:
            prx_lst = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located((By.XPATH, '//table[@id="proxy_list"]'))
            )
            rows_count = len(driver.find_elements(by=By.XPATH, value='//table[@id="proxy_list"]/tbody/tr'))
        except:
            print(SERVICE_NAME, "Page changed, data not found on page.")
            return None
            
        for row_num in range(rows_count):
            try:
                ip = driver.find_element(by=By.XPATH, value='//table[@id="proxy_list"]/tbody/tr[' + str(row_num+1) + ']/td[1]')
                port = driver.find_element(by=By.XPATH, value='//table[@id="proxy_list"]/tbody/tr[' + str(row_num+1) + ']/td[2]')
                export_proxies.add(ip.text + ":" + port.text)
            except:
                continue


    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(
        get_proxy_free_proxy_cz()
    )