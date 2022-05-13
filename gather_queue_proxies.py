def gather_queue_proxies( current_queue: list = [],
                            scan_manual_proxies: bool = True,
                            rescan_old_proxies: bool = True,
                            collect_queue_history: bool = True
                            ) -> set:
    # CRAWLING LOCAL FILES MODULE
    import crawl_local_proxies
    # ===========================

    # CREATE UNIQUE PROXIES SET
    queue_proxies = set(current_queue)
    # =========================

   # CREATE UNIQUE PROXIES SET
    old_proxies = []
    manual_proxies = []
    # =========================

    # OLD PROXIES / WORK DIR SET EARLIER TO SCRIPT DIR
    if rescan_old_proxies:
        oldLen = len(queue_proxies)
        old_proxies = crawl_local_proxies.get_proxies_from_file(filename='proxies_.txt')
        queue_proxies.update( old_proxies )
        print("Added", len(queue_proxies) - oldLen, "unique new proxies.")
    # ================================================
    # MANUAL PROXIES / WORK DIR SET EARLIER TO SCRIPT DIR
    if scan_manual_proxies:
        oldLen = len(queue_proxies)
        manual_proxies = crawl_local_proxies.get_proxies_from_file(filename='proxies_manual_queue.txt')
        queue_proxies.update( manual_proxies )
        print("Added", len(queue_proxies) - oldLen, "unique new proxies.")
    # ===================================================
    # COLLECT PROXIES HISTORY FOR FUTURE RECHECK / WORK DIR SET EARLIER TO SCRIPT DIR
    if collect_queue_history:
        oldLen = len(queue_proxies)
        queue_history_proxies = crawl_local_proxies.get_proxies_from_file(filename='proxies_queue_unchecked.txt')
        queue_proxies.update( queue_history_proxies )
        print("Added", len(queue_proxies) - oldLen, "unique new proxies.")
    # ===============================================================================

    # REMOVE DUBLICATES
    # TWO TYPES OF PROXY: WITHOUT AND WITH TYPE TYPE://IP_ADDR:PORT
    detected_proxies = [proxy.split("://")[-1] for proxy in queue_proxies if "://" in proxy]
    for proxy in detected_proxies:
        queue_proxies.discard(proxy)
    # =================

    # SAVE ALL PARCED PROXIES TO QUEUE FILE
    # WORK DIR SET EARLIER TO SCRIPT DIR
    # SKIP < IF NO NEW PROXIES WERE ADDED
    if len(queue_proxies) > len(old_proxies) + len(manual_proxies):
        print("\nSaving", len(queue_proxies), "unchecked proxies", "to proxies_queue_unchecked.txt")
        with open('proxies_queue_unchecked.txt', 'w') as f:
            f.writelines("\n".join(queue_proxies))
    # ====================================
    
    return queue_proxies


if __name__ == "__main__":
    print(
        gather_queue_proxies()
        )
