def ping_proxies(hosts_list: list = [], debug=False) -> set:
    import subprocess
    import concurrent.futures
    from tqdm import tqdm

    TMOUT = 3

    export_proxies = set()

    def ping(host):
        response = subprocess.call(
            ["ping", "-c 2", "-t " + str(TMOUT), host.split(":")[0]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        if response == 0:
            export_proxies.add(host)
            # print(host)

    if not hosts_list:
        try:
            import parce_local_proxies

            raw_proxies = parce_local_proxies.get_proxies_from_file(
                "proxies_queue_unchecked.txt"
            )
            ips = [x.split("://")[-1].split(":")[0] for x in raw_proxies]
        except Exception:
            return

    # progress bar
    with tqdm(
        total=len(ips), ascii="░▒█", unit="prx", smoothing=0, disable=debug
    ) as pbar:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=35
        ) as executor:  # no "max_workers" for optimally defined number of threads
            futures = [executor.submit(ping, proxy) for proxy in ips]
            res = set()
            for future in concurrent.futures.as_completed(futures):
                res.add(future.result())
                # progress bar update
                pbar.update()

    export_proxies.update(res)

    print("Pingable proxies:", len(export_proxies), "/", len(ips))
    return export_proxies


if __name__ == "__main__":
    print(ping_proxies())
