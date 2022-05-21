def crawl_online_proxy_services(existing_proxies: list = []) -> set:
    # BUILT-INS
    import concurrent.futures  # multithreading

    # =========

    # CRAWLING MODULES
    import crawlweb_free_proxy_cz
    import crawlweb_freeproxy_world
    import crawlweb_good_proxies_ru
    import crawlweb_online_proxy_ru
    import crawlweb_premproxy_com
    import crawlweb_proxy_nova_com
    import crawlweb_proxy_tools_com
    import crawlweb_proxydb_net
    import crawlweb_proxydocker_com
    import crawlweb_proxyranker_com
    import crawlweb_proxyscan_io
    import crawlweb_proxyscrape_com
    import crawlweb_socks_proxy_net
    import crawlweb_spys_one
    import crawlweb_spyss_me

    # ==============

    # CREATE A SET OF ALWAYS UNIQUE PROXIES
    export_proxies = set()
    parced_proxies = set()
    # =====================================
    oldLen = len(existing_proxies)

    # STAR PARCING SOURCES IN MULTITHREADING
    print("\nParcing websites...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        res = set()
        futures = [
            executor.submit(crawlweb_free_proxy_cz.free_proxy_cz),  # bans a lot
            executor.submit(crawlweb_freeproxy_world.freeproxy_world),
            executor.submit(crawlweb_good_proxies_ru.good_proxies_ru, country="ru"),
            executor.submit(crawlweb_online_proxy_ru.online_proxy_ru),
            executor.submit(crawlweb_premproxy_com.premproxy_com),
            executor.submit(crawlweb_proxy_nova_com.proxy_nova_com),
            executor.submit(crawlweb_proxy_tools_com.proxy_tools_com),  # captcha
            executor.submit(crawlweb_proxydb_net.proxydb_net),  # captcha
            executor.submit(crawlweb_proxydocker_com.proxydocker_com),
            executor.submit(crawlweb_proxyranker_com.proxyranker_com),
            executor.submit(crawlweb_proxyscan_io.proxyscan_io, country="ru"),
            executor.submit(crawlweb_proxyscrape_com.proxyscrape_com),
            executor.submit(crawlweb_socks_proxy_net.socks_proxy_net),
            executor.submit(crawlweb_spys_one.spys_one),  # minimized windows hides data
            executor.submit(crawlweb_spyss_me.spyss_github, country="RU"),
            ##################### PARCE PROXY TYPES !! #######################
            # https://geonode.com/free-proxy-list/
            # https://proxyline.net/en/besplatnye-onlajn-proksi-servera/
            # https://proxyservers.pro/proxy/list/country/RU/order/updated/order_dir/desc/page/1
            # https://www.proxyhub.me/en/ru-free-proxy-list.html
            # https://freeproxylist.cc/online/Russia/ ## NAH - no ssl search, no protocol
            # https://premiumproxy.net/top-country-proxy-list/RU-Russia ## COPY OF spys_one
        ]
        for future in concurrent.futures.as_completed(futures):
            parced_proxies.update(future.result() if future.result() else set())
    # ====================================

    export_proxies.update(parced_proxies, existing_proxies)

    # REMOVE DUBLICATES PROXIES WITHOUT TYPE://
    # TWO TYPES OF PROXY: WITHOUT AND WITH TYPE TYPE://IP_ADDR:PORT
    detected_proxies = [
        proxy.split("://")[-1] for proxy in export_proxies if "://" in proxy
    ]
    export_proxies = export_proxies - set(detected_proxies)
    # =================

    print("\nParced", len(parced_proxies), "proxies.")
    print("Added", len(export_proxies) - oldLen, "new unique proxies.")

    return export_proxies


if __name__ == "__main__":
    proxies = []
    print(
        crawl_online_proxy_services(existing_proxies=proxies),
    )
