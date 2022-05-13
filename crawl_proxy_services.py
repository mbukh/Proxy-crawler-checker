def crawl_online_proxy_services() -> set:
    # BUILT-INS
    import concurrent.futures # multithreading
    # =========
    
    # CRAWLING MODULES
    import parce_free_proxy_cz
    import parce_proxy_freeproxy_world
    import parce_proxy_good_proxies_ru
    import parce_proxy_nova_com
    import parce_proxy_online_proxy_ru
    import parce_proxy_premproxy_com
    import parce_proxy_proxy_tools_com
    import parce_proxy_proxydb_net
    import parce_proxy_proxyranker_com
    import parce_proxy_proxyscan_io
    import parce_proxy_proxyscrape_com
    import parce_proxy_spys_one
    import parce_spyss_me
    # ==============

    # CREATE A SET OF ALWAYS UNIQUE PROXIES
    queue_proxies = set()
    # =====================================

    # STAR PARCING SOURCES IN MULTITHREADING 
    print("\nParcing websites...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        res = set()
        futures = [
                # executor.submit( parce_free_proxy_cz.get_proxy_free_proxy_cz ), # bans a lot
                executor.submit( parce_proxy_proxy_tools_com.get_proxy_proxy_tools_com, minimized = False ),  # captcha
                executor.submit( parce_proxy_freeproxy_world.get_proxy_freeproxy_world ),
                executor.submit( parce_proxy_good_proxies_ru.parce_proxy_good_proxies_ru, country='ru' ),
                executor.submit( parce_proxy_nova_com.get_proxy_nova_com ),
                executor.submit( parce_proxy_online_proxy_ru.get_proxy_online_proxy_ru ),
                executor.submit( parce_proxy_premproxy_com.get_proxy_premproxy_com ),
                executor.submit( parce_proxy_proxyranker_com.get_proxy_proxyranker_com ),
                executor.submit( parce_proxy_proxyscan_io.parce_proxy_proxyscan_io, country='ru' ),
                executor.submit( parce_proxy_proxyscrape_com.parce_proxyscrape_com ),
                executor.submit( parce_proxy_spys_one.get_proxy_spys_one, minimized = False), # minimized windows hides data
                executor.submit( parce_spyss_me.get_proxy_spyss, country = 'RU' ),
                executor.submit( parce_proxy_proxydb_net.get_proxy_proxydb_net, minimized = False ), # captcha
                ]
        for future in concurrent.futures.as_completed(futures):
            queue_proxies.update( future.result() if future.result() else set() )
    # ====================================
    
    if len(queue_proxies):
        print("\nParced", len(queue_proxies), "unique proxies\n")

    return queue_proxies

if __name__ == "__main__":
    print(
        crawl_online_proxy_services()
        )