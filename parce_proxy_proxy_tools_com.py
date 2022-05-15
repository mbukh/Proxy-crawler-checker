def get_proxy_proxy_tools_com(minimized: bool = False, showBrowser: bool = True) -> set:
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

    url = 'https://proxy-tools.com/proxy/ru'

    options = Options()
    options.headless = not showBrowser
    options.add_argument("--window-position=1200,100")
    options.add_argument("--window-size=1024,768")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=logging.WARNING, print_first_line=False).install()), options=options)
    except:
        print(SERVICE_NAME, "Can't connect to the server.")
        return None
        
    if minimized:
        driver.minimize_window() # if no user interaction needed, but browser must be open

    try:
        driver.set_page_load_timeout(TMOUT)
        driver.get(url)
    except:
        print(SERVICE_NAME, "Can't connect to a page ", url)
        return None
    

                                # ADD PAGING !!


    # if captcha exists - pass it
    max_tries = 1
    tried = 0
    while True:
        try:
            request_ports = WebDriverWait(driver, TMOUT).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='ct-main']/main/table/tbody/tr[1]/td[2]/a"))
                )
            actions = ActionChains(driver)
            actions.move_to_element(request_ports)
            actions.click(request_ports)
            actions.perform()
            sleep(20)
            if tried == max_tries:
                print(SERVICE_NAME, "captcha needed.")
                return None
            tried += 1
        except:
            break

    try:
        table_proxy = WebDriverWait(driver, TMOUT).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='ct-main']/main/table/tbody/tr"))
            )
        rows_count = len(driver.find_elements(by=By.XPATH, value="//div[@id='ct-main']/main/table/tbody/tr"))
    except:
        print(SERVICE_NAME, "Page changed, data not found on page.")
        return None

    for row_num in range(rows_count):
        try:
            ip = driver.find_element(by=By.XPATH, value="//*[@id='ct-main']/main/table/tbody/tr[" + str(row_num+1) + ']/td[1]')
            port = driver.find_element(by=By.XPATH, value="//*[@id='ct-main']/main/table/tbody/tr[" + str(row_num+1) + ']/td[2]')
            export_proxies.add(ip.text + ":" + port.text)
        except:
            continue

    driver.quit()

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(
        get_proxy_proxy_tools_com()
    )
