from turtle import update


def crawl_online_proxy_services(existing_proxies: list = []) -> set:
    # BUILT-INS
    import concurrent.futures  # multithreading

    # =========

    # CRAWLING MODULES
    import crawlweb_free_proxy_cz
    import crawlweb_freeproxy_world
    import crawlweb_good_proxies_ru
    import crawlweb_proxy_nova_com
    import crawlweb_online_proxy_ru
    import crawlweb_premproxy_com
    import crawlweb_proxy_tools_com
    import crawlweb_proxydb_net
    import crawlweb_proxyranker_com
    import crawlweb_proxyscan_io
    import crawlweb_proxyscrape_com
    import crawlweb_spys_one
    import crawlweb_spyss_me

    # ==============

    # CREATE A SET OF ALWAYS UNIQUE PROXIES
    queue_proxies = set()
    # =====================================
    oldLen = len(existing_proxies)

    # STAR PARCING SOURCES IN MULTITHREADING
    print("\nParcing websites...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        res = set()
        futures = [
            # executor.submit( parce_free_proxy_cz.free_proxy_cz ), # bans a lot
            executor.submit(crawlweb_freeproxy_world.freeproxy_world),
            executor.submit(
                crawlweb_proxy_tools_com.proxy_tools_com, minimized=False
            ),  # captcha
            executor.submit(crawlweb_good_proxies_ru.good_proxies_ru, country="ru"),
            executor.submit(crawlweb_proxy_nova_com.proxy_nova_com),
            executor.submit(crawlweb_online_proxy_ru.online_proxy_ru),
            executor.submit(crawlweb_premproxy_com.premproxy_com),
            executor.submit(crawlweb_proxyranker_com.proxyranker_com),
            executor.submit(crawlweb_proxyscan_io.proxyscan_io, country="ru"),
            executor.submit(crawlweb_proxyscrape_com.proxyscrape_com),
            executor.submit(
                crawlweb_spys_one.spys_one, minimized=False
            ),  # minimized windows hides data
            executor.submit(crawlweb_spyss_me.spyss_github, country="RU"),
            executor.submit(
                crawlweb_proxydb_net.proxydb_net, minimized=False
            ),  # captcha
            ##################### PARCE PROXY TYPES !! #######################
            # https://www.socks-proxy.net/ "Russian Federation"
            # https://freeproxylist.cc/online/Russia/
            # https://www.proxydocker.com/en/proxylist/country/Russia
            # https://www.proxyhub.me/en/ru-free-proxy-list.html
            # https://premiumproxy.net/top-country-proxy-list/RU-Russia
            # https://geonode.com/free-proxy-list/
            # https://proxyline.net/en/besplatnye-onlajn-proksi-servera/
            # https://proxyservers.pro/proxy/list/country/RU/order/updated/order_dir/desc/page/1
        ]
        for future in concurrent.futures.as_completed(futures):
            queue_proxies.update(future.result() if future.result() else set())
    # ====================================

    # REMOVE EXISTING PROXIES WITHOUT TYPE://
    queue_proxies.difference_update([x.split("://")[-1] for x in existing_proxies])

    # RETURN EXISTING PROXIES CONTAITING TYPE://
    queue_proxies.update(existing_proxies)

    if len(queue_proxies):
        print("\nParced", len(queue_proxies), "unique proxies.")
        print("Added", len(queue_proxies) - oldLen, "new unique proxies.\n")

    return queue_proxies


if __name__ == "__main__":
    proxies = []
    print(crawl_online_proxy_services(existing_proxies=proxies))
