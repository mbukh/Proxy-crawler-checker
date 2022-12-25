def geonode_com(
    country_code: str = "ru",
) -> set:
    import requests
    from time import sleep

    SERVICE_NAME = "Geonode.com:"
    TMOUT = 20
    export_proxies = set()

    urls = [
        (
            "all",
            "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&country="
            + country_code.upper()
            + "&anonymityLevel=elite&anonymityLevel=anonymous",
        )
    ]

    for protocol, url in urls:
        try:
            resp = requests.get(url, timeout=TMOUT)
            if resp.status_code == 200:
                export_proxies.update(
                    [
                        x["protocols"][0].lower() + "://" + x["ip"] + ":" + x["port"]
                        for x in resp.json()["data"]
                    ]
                )
            else:
                print(SERVICE_NAME, "url response error", url)
        except Exception as e:
            print(SERVICE_NAME, "Can't connect to the server.")
            return None

        sleep(5)

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    pr_list = geonode_com(
        country_code="il",
    )
    for pr in pr_list:
        print(pr)
