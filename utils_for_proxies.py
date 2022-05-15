def filter_proxies(queue_proxies: list = []) -> set:

    queue_proxies = set(queue_proxies)

    # SERVICE FOR CHECKING IP COUNTRY IN MULTITHREADS
    # import get_proxy_country
    # print("\nDetecting proxy country\n")
    # queue_proxies = get_proxy_country.get_proxies_country(queue_proxies, 'RU')
    # ===============================================

    # SERVICE FOR PINGING IPS IN MULTITHREADS
    # (might be used to recheck old proxies)
    # import ping_proxies
    # print("\n\nPinging proxies")
    # queue_proxies = ping_proxies.ping_proxies(queue_proxies)
    # =======================================

    return queue_proxies


if __name__ == "__main__":
    print(filter_proxies())
