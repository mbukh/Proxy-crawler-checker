def proxyscan_io(country: str = "RU") -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Proxyscan.io:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        (
            "all",
            "https://www.proxyscan.io/api/proxy?limit=100&type=socks4,socks5,https&format=json&country="
            + country.lower(),
        )
    ]

    for protocol, url in urls:
        try:
            resp = requests.get(url, timeout=TMOUT)
            if resp.status_code == 200:
                export_proxies.update(
                    [
                        x["Type"][0].lower() + "://" + x["Ip"] + str(x["Port"])
                        for x in resp.json()
                    ]
                )
            else:
                print(SERVICE_NAME, "url responce error", url)
        except Exception as e:
            print(SERVICE_NAME, "Can't connect to the server.")
            return None

        sleep(5)

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(proxyscan_io(country="ru"))
