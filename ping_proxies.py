def ping_proxies(hosts_list: list = []) -> set:
    import subprocess
    import concurrent.futures

    TMOUT = 20

    export_proxies = []

    def ping(host):
        response = subprocess.call(
            ["ping", "-c 2", "-t " + str(TMOUT), host.split(":")[0]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        if response == 0:
            export_proxies.append(host)
            # print(host)

    if not hosts_list:
        try:
            txt_file = open("proxies_queue_unchecked.txt", "r")
            hosts_list = txt_file.read().splitlines()  # last element not \n
        except Exception:
            return

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=35
    ) as executor:  # no "max_workers" for optimally defined number of threads
        res = [executor.submit(ping, proxy) for proxy in hosts_list]
        concurrent.futures.wait(res)

    export_proxies = set(export_proxies)

    print("Pingable proxies:", len(export_proxies), "/", len(hosts_list))
    return export_proxies


if __name__ == "__main__":
    print(ping_proxies())
