def parce_proxyscrape_com() -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Proxyscrape.com:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=RU&ssl=yes&anonymity=all&simplified=true',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=RU&simplified=true',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=RU&simplified=true',
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

    export_proxies = set([x.rstrip() for x in data if ":" in x])
    
    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(
        parce_proxyscrape_com()
    )