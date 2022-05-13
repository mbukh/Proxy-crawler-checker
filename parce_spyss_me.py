def get_proxy_spyss(country: str = "RU") -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Spys.me:"
    TMOUT = 20
    export_proxies = set()

    urls = [
            'https://spys.me/proxy.txt',
            'https://spys.me/socks.txt',
            ]

    data = set()
    
    for url in urls:
        try:
            resp = requests.get(url, timeout=TMOUT)
            if resp.status_code == 200:
                data.update(resp.text.split("\n"))
            else:
                print(SERVICE_NAME, "url responce error", url)
        except:
            print(SERVICE_NAME, "Can't connect to the server.")
            return None
        sleep(5)

    export_proxies = set([x.split()[0] for x in data if (x.find(country.upper()) != -1)]) #  and (x.find("-S") != -1) / SSL SUPPORT ONLY

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(
        get_proxy_spyss()
    )