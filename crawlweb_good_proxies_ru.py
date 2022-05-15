def good_proxies_ru(country: str = "RU") -> set:
    import requests

    SERVICE_NAME = "Good-proxies.ru"
    TMOUT = 20
    export_proxies = set()

    url = (
        "https://api.good-proxies.ru/getfree.php?count=100&ping=8000&time=600&works=100&country%5B%5D="
        + country.lower()
        + "&key=freeproxy"
    )

    try:
        resp = requests.get(url, timeout=TMOUT)
        if resp.status_code == 200:
            data = resp.text.split("\n")
            export_proxies.update(
                [x for x in data if ":" in x and not ("script" in x or "span" in x)]
            )
        else:
            print(SERVICE_NAME, "url responce error", url)

    except Exception as e:
        print(SERVICE_NAME, "Can't connect to the server.")
        return None

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(good_proxies_ru(country="RU"))
