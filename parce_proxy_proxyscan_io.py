def parce_proxy_proxyscan_io(country: str = 'RU') -> set:
    import requests

    SERVICE_NAME = "Proxyscan.io:"
    TMOUT = 20
    export_proxies = set()
    
    url ='https://www.proxyscan.io/api/proxy?limit=100&type=socks4,socks5,https&format=txt&country='+country.lower()

    try:
        resp = requests.get(url, timeout=TMOUT)
        if resp.status_code == 200:
            data = resp.text.split("\n")
            export_proxies.update([x for x in data if ":" in x])
        else:
            print(SERVICE_NAME, "url responce error", url)

    except Exception as e:
        print(SERVICE_NAME, "Can't connect to the server.")
        return None

    print(SERVICE_NAME, len(export_proxies))
    return export_proxies


if __name__ == "__main__":
    print(
        parce_proxy_proxyscan_io(country='ru')
    )