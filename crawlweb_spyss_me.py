def spyss_github(country: str = "RU") -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Spys.me:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        ("all", "https://spys.me/socks.txt"),
        ("all", "https://spys.me/proxy.txt"),
    ]

    for proxy_type, url in urls:
        try:
            resp = requests.get(url, timeout=TMOUT)
            if resp.status_code == 200:
                export_proxies.update(
                    [
                        x.split()[0]
                        for x in resp.text.split("\n")
                        if (x.find(country.upper()) != -1)
                        # and (x.find("-S") != -1) / SSL SUPPORT ONLY
                    ]
                )
            else:
                print(SERVICE_NAME, "url responce error", url)
        except:
            print(SERVICE_NAME, "Can't connect to the server.")
            return None
        sleep(5)

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(spyss_github())
