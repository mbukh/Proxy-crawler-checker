def gather_queue_proxies(
    current_queue: list = [],
    collect_queue_history: bool = True,
    collect_checked_proxies: bool = True,
    scan_manual_proxies: bool = True,
    save_queue_file: bool = False,
) -> set:
    # CRAWLING LOCAL FILES MODULE
    import parce_local_proxies

    # ===========================

    # CREATE UNIQUE PROXIES SET
    queue_proxies = set(current_queue)
    # =========================

    # CREATE UNIQUE PROXIES SET
    old_proxies = []
    manual_proxies = []
    # =========================

    def remove_duplicates(queue_proxies: list = []):
        export_proxies = set(queue_proxies)
        # REMOVE DUBLICATES PROXIES WITHOUT TYPE://
        # TWO TYPES OF PROXY: WITHOUT AND WITH TYPE TYPE://IP_ADDR:PORT
        detected_proxies = [
            proxy.split("://")[-1] for proxy in queue_proxies if "://" in proxy
        ]
        export_proxies.difference_update(detected_proxies)
        return export_proxies
        # =================

    print("\n[Local files proxies gathering...]")

    # COLLECT PROXIES HISTORY FOR FUTURE RECHECK / WORK DIR SET EARLIER TO SCRIPT DIR
    if collect_queue_history:
        oldLen = len(queue_proxies)
        queue_history_proxies = parce_local_proxies.get_proxies_from_file(
            filename="proxies_queue_unchecked.txt",
        )
        queue_proxies.update(queue_history_proxies)
        queue_proxies = remove_duplicates(queue_proxies)
        print("Added", len(queue_proxies) - oldLen, "proxies from an unchecked queue.")
    # ===============================================================================
    # OLD PROXIES / WORK DIR SET EARLIER TO SCRIPT DIR
    if collect_checked_proxies:
        oldLen = len(queue_proxies)
        old_proxies = parce_local_proxies.get_proxies_from_file(
            filename="proxies_.txt",
        )
        queue_proxies.update(old_proxies)
        queue_proxies = remove_duplicates(queue_proxies)
        print(
            "Updated type to existing proxies. Added",
            str(len(queue_proxies) - oldLen),
            "unique new proxies.",
        )
    # ================================================
    # MANUAL PROXIES / WORK DIR SET EARLIER TO SCRIPT DIR
    if scan_manual_proxies:
        oldLen = len(queue_proxies)
        manual_proxies = parce_local_proxies.get_proxies_from_file(
            filename="proxies_manual_queue.txt",
        )
        queue_proxies.update(manual_proxies)
        queue_proxies = remove_duplicates(queue_proxies)
        print("Added", len(queue_proxies) - oldLen, "unique new proxies.")
    # ===================================================

    # SAVE ALL PARCED PROXIES TO QUEUE FILE
    # WORK DIR SET EARLIER TO SCRIPT DIR
    # SKIP < IF NO NEW PROXIES WERE ADDED
    if save_queue_file:
        if len(queue_proxies) > len(old_proxies) + len(manual_proxies):
            print(
                "\nSaving",
                len(queue_proxies),
                "unchecked proxies",
                "to proxies_queue_unchecked.txt",
            )
            with open("proxies_queue_unchecked.txt", "w") as f:
                f.writelines("\n".join(queue_proxies))
    # ====================================

    print("[Total]", len(queue_proxies), "local unique proxies.")

    return queue_proxies


if __name__ == "__main__":
    print(
        len(
            gather_queue_proxies(
                save_queue_file=False,
            )
        ),
    )
