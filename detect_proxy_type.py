def detect_proxies_type(
    queue_proxies: list = [],
    save_anonymous: bool = True,
    debug: bool = False,
    concurrent_checks: int = 35,
) -> set:
    # POSSIBLE FORMATS FOR hosts_list:
    # A) IP_ADDR:PORT
    # B) TYPE://IP_ADDR:PORT

    import requests
    import concurrent.futures
    from random import sample, choice
    from tqdm import tqdm

    # DISABLE VERIFYE=FALSE WARNING
    from urllib3 import disable_warnings

    disable_warnings()
    # =============================
    TMOUT = 4
    CHECK_URLS_COUNT = 6
    SUCCESS_TIMES = 1

    export_proxies = set()
    anonym_proxies = set()

    try:
        my_ip = requests.get("https://ipinfo.io/ip", timeout=TMOUT)
        my_ip = my_ip.text.split(":")[0]
    except Exception as e:
        try:
            my_ip = requests.get("https://api.ipify.org/", timeout=TMOUT)
            my_ip = my_ip.text.split(":")[0]
        except Exception as e:
            my_ip = None

    # FUNCTION CHECKS ONE PROXY AND RETURNS TYPE://IP:PORT
    def checkProxy(proxy: str = "") -> str:
        successCount = 0  # AT LEAST TWO SERVICES REPLY OK TO DETECT A WORKING PROXY

        # CHECK IF PROXY CONSISTS OF TYPE -> USE IT
        if "://" in proxy:
            knownType, proxy_ipport = proxy.split("://")
        else:
            knownType = None
            proxy_ipport = proxy

        headers = [
            # from fake_useragent import UserAgent
            # ua = UserAgent()
            # ua.chrome
            # ua.random
            # or
            # from random_user_agent.user_agent import UserAgent
            # https://github.com/Luqman-Ud-Din/random_user_agent
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1"
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            },
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.3; rv:100.0) Gecko/20100101 Firefox/100.0"
            },
            {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/100.0 Mobile/15E148 Safari/605.1.15"
            },
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/86.0.4363.23"
            },
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/86.0.4363.23"
            },
        ]
        # CHECK SERVER APIs
        checkUrls = [
            "https://api.ipify.org/",  # txt or https://api.ipify.org?format=json
            "https://api.bigdatacloud.net/data/client-ip",  # json
            "https://api.ip.sb/ip",  # txt
            "https://api.myip.com/",
            "https://api.myip.la",  # txt or https://api.myip.la/cn?json
            "https://curlmyip.net/",  # txt
            "https://crymyip.com/",
            "https://checkip.dns.he.net/",  # txt
            "https://checkip.amazonaws.com/",  # txt
            "https://dnswatch.info/what's-my-ip",
            "https://httpbin.org/ip",  # ± txt
            "https://icanhazip.com/",  # txt
            "https://ident.me/",  # txt or https://ident.me/json
            "https://ifconfig.me/",
            "https://ipinfo.io/ip",  # txt
            "https://ipecho.net/plain",  # txt
            "https://ip4only.me/api/",  # ± txt
            "https://ip-api.com/json/",
            "https://jsonip.com/",
            "https://l2.io/ip",  # txt or https://www.l2.io/ip.json
            "https://trackip.net/ip",  # txt or https://www.trackip.net/ip?json
            "https://trackip.net/pfsense",  # ± txt
        ]
        # get different random servers
        randomHeaders = choice(headers)
        randomCheckers = sample(checkUrls, CHECK_URLS_COUNT)
        if not knownType:
            protocols = [  # from the most popular to the least
                {"https": "socks4://" + proxy_ipport},
                {"https": "socks5://" + proxy_ipport},
                {"https": "https://" + proxy_ipport},
                # {"http" : "http://"}, # HTTP PROXY NOT DETECTING/ BEING BYPASSED BY REQUESTS.GET ??
            ]
        else:
            protocols = [{"https": knownType + "://" + proxy_ipport}]
        # server API loop
        for checkerUrl in randomCheckers:
            # protocol loop
            for protocol in protocols:
                try:
                    reqResponce = requests.get(
                        checkerUrl,
                        proxies=protocol,
                        headers=randomHeaders,
                        verify=False,
                        timeout=TMOUT,
                    )
                    if reqResponce.status_code == 200 and reqResponce.text:
                        # proxy anonymity
                        if my_ip and my_ip not in reqResponce.text:
                            if debug:
                                print(
                                    "[ Anonymous ]",
                                    my_ip,
                                    " => ",
                                    protocol,
                                    "returned by",
                                    checkerUrl,
                                )
                            anonym_proxies.add(
                                protocol[list(protocol)[0]]
                            )  # FIRST ELEMENT VALUE IN DICT
                        if debug:
                            print(
                                "[SUCCESS]:",
                                "Connected to",
                                checkerUrl,
                                "via proxy",
                                protocol,
                            )
                            # print("TEXT: ", reqResponce.text.replace("\n","").replace("\t"," ").replace("  ",""))
                        successCount += 1
                        if successCount >= SUCCESS_TIMES:
                            return protocol[
                                list(protocol)[0]
                            ]  # FIRST ELEMENT VALUE IN DICT
                    else:
                        if debug:
                            print(
                                "[STATUS_CODE]:",
                                reqResponce.status_code,
                                ", page:",
                                checkerUrl,
                                "via proxy",
                                protocol,
                            )
                        pass
                except Exception as e:
                    if debug:
                        print(
                            "[ERROR]:",
                            "Couldn't connect to",
                            checkerUrl,
                            "via proxy",
                            protocol,
                        )
                    pass
        if debug:
            print("[ERROR]:", proxy, "[Proxy dead]")
        return None

    # hosts_list not set ot empty
    if not queue_proxies:
        try:
            import gather_queue_proxies

            queue_proxies = gather_queue_proxies.gather_queue_proxies(
                scan_manual_proxies=True,
                collect_checked_proxies=False,
                collect_queue_history=False,
                save_queue_file=False,
            )
        except Exception:
            return None

    # progress bar
    with tqdm(
        total=len(queue_proxies), ascii="░▒█", unit="prx", smoothing=0, disable=debug
    ) as pbar:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=concurrent_checks
        ) as executor:  # no "max_workers" for optimally defined number of threads
            futures = [executor.submit(checkProxy, proxy) for proxy in queue_proxies]
            res = set()
            for future in concurrent.futures.as_completed(futures):
                res.add(future.result())
                # progress bar update
                pbar.update()

    # save anonymous proxy list
    if save_anonymous and anonym_proxies:
        print("Writing proxy_anonymous.txt", len(anonym_proxies), "proxies")
        with open("proxy_anonymous.txt", "w") as f:
            f.writelines("\n".join(anonym_proxies))

    export_proxies.update(res)

    # REMOVE EMPTY. NO DUPLICATES IN SET AFTER CHECKING TYPE
    export_proxies = [proxy for proxy in export_proxies if proxy]
    # ======================================================

    print(
        "Working proxies",
        len(export_proxies),
        "/",
        len(queue_proxies),
        ", Anonymous:",
        len(anonym_proxies) if my_ip else "couldn't check",
    )
    return export_proxies


if __name__ == "__main__":
    proxies = []
    print(
        detect_proxies_type(
            queue_proxies=proxies,
            save_anonymous=False,
            debug=False,
            concurrent_checks=35,
        )
    )
