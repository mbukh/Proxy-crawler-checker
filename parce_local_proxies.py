def get_proxies_from_file(filename: str = "proxies_.txt") -> set():
    queue_proxies = set()
    print("Reading from", filename)
    try:
        # WORK DIR SET EARLIER TO SCRIPT DIR
        txt_file = open(filename, "r")
        hosts_list = txt_file.read().splitlines()  # last element not \n
        queue_proxies.update(hosts_list)
        queue_proxies = [x for x in queue_proxies if ":" in x]
        print("Found", len(queue_proxies), "proxies.")
    except Exception as e:
        print("Error getting from", filename, "\n", e)
    # ======================================================
    return queue_proxies


if __name__ == "__main__":
    print(
        get_proxies_from_file(),
    )
