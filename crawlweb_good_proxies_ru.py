def good_proxies_ru(country: str = "RU") -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Good-proxies.ru"
    TMOUT = 20
    export_proxies = set()

    urls = [
        (
            "socks4",
            "https://api.good-proxies.ru/getfree.php?type%5Bsocks4%5D=on&anon%5B%27transparent%27%5D=on&anon%5B%27anonymous%27%5D=on&anon%5B%27elite%27%5D=on&count=100&ping=8000&time=600&works=90&country%5B%5D="
            + country.lower()
            + "&key=freeproxy",
        ),
        (
            "socks5",
            "https://api.good-proxies.ru/getfree.php?type%5Bsocks5%5D=on&anon%5B%27transparent%27%5D=on&anon%5B%27anonymous%27%5D=on&anon%5B%27elite%27%5D=on&count=100&ping=8000&time=600&works=90&country%5B%5D="
            + country.lower()
            + "&key=freeproxy",
        ),
        (
            "https",
            "https://api.good-proxies.ru/getfree.php?access%5B%27supportsHttps%27%5D=on&anon%5B%27transparent%27%5D=on&anon%5B%27anonymous%27%5D=on&anon%5B%27elite%27%5D=on&count=100&ping=8000&time=600&works=90&country%5B%5D="
            + country.lower()
            + "&key=freeproxy",
        ),
    ]

    for proxy_type, url in urls:
        try:
            resp = requests.get(url, timeout=TMOUT)
            if resp.status_code == 200:
                export_proxies.update(
                    [
                        proxy_type + "://" + x
                        for x in resp.text.split("\n")
                        if ":" in x and not "<" in x
                    ]
                )
            else:
                print(SERVICE_NAME, "url responce error", url)
        except Exception:
            print(SERVICE_NAME, "Can't connect to the server.")
            return None
        sleep(30)

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(good_proxies_ru(country="RU"))
