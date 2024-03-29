def proxyscrape_com(
    country_code: str = "ru",
) -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Proxyscrape.com:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        (
            "https",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country="
            + country_code.upper()
            + "&ssl=yes&anonymity=all&simplified=true",
        ),
        (
            "socks4",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country="
            + country_code.upper()
            + "&simplified=true",
        ),
        (
            "socks5",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country="
            + country_code.upper()
            + "&simplified=true",
        ),
    ]

    for proxy_type, url in urls:
        try:
            resp = requests.get(url, timeout=TMOUT)
            if resp.status_code == 200:
                export_proxies.update(
                    [proxy_type + "://" + x.rstrip() for x in resp.text.split("\n") if x]
                )
            else:
                print(SERVICE_NAME, "url response error", url)
        except Exception:
            print(SERVICE_NAME, "Can't connect to the server.")
            return None

        sleep(5)

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    pr_list = proxyscrape_com(
        country_code="il",
    )
    for pr in pr_list:
        print(pr)
