def get_proxies_country(hosts_list: list = [], country: str = "RU") -> set:
    import requests
    import json
    import concurrent.futures
    from time import sleep

    TMOUT = 20

    export_proxies = []

    def get_county(host):
        ip = host.split(":")[0]
        # URL to send the request to
        request_url = "https://geolocation-db.com/jsonp/" + ip
        # Send request and decode the result
        response = requests.get(request_url, timeout=TMOUT)
        result = response.content.decode()
        # Clean the returned string so it just contains the dictionary data for the IP address
        result = result.split("(")[1].strip(")")
        # Convert this data into a dictionary
        result = json.loads(result)
        try:
            if result["country_code"] == country:
                export_proxies.append(host)
        except Exception:
            return
        sleep(0.5)  # to prevent API overload and block

    if not hosts_list:
        try:
            txt_file = open("proxies_queue_unchecked.txt", "r")
            hosts_list = set(txt_file.read().splitlines())  # last element not \n
        except Exception:
            return

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=10
    ) as executor:  # no "max_workers" for optimally defined number of threads
        res = [executor.submit(get_county, proxy) for proxy in hosts_list]
        concurrent.futures.wait(res)

    export_proxies = set(export_proxies)

    print("Country", country, ":", len(export_proxies), "/", len(hosts_list))
    return export_proxies


if __name__ == "__main__":
    print(get_proxies_country())
