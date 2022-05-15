def main() -> int:
    # BUILT-INS
    import os
    from time import sleep, time
    from shutil import copyfile  # copy file
    from datetime import datetime

    # ========

    # PROGRESS BAR
    try:
        import tqdm  # progress bar
    except Exception as e:
        print("Run: python -m pip install tqdm")
        return -1
    # ============

    # DETECTING PROXIES ENGINE
    try:
        import gather_queue_proxies
    except:
        print("Missing main gathering module 'gather_queue_proxies.py'.")
        return -1
    # ========================
    # DETECTING PROXIES ENGINE
    try:
        import detect_proxy_type
    except:
        print("Missing main proxy detection module 'detect_proxy_type.py'.")
        return -1
    # ========================

    # CRAWLING MODULE
    try:
        import crawl_proxy_services

        CRWALING_MODULE = True
    except Exception as e:
        CRWALING_MODULE = False
        print("Missing crawling module. Manual checks and rechecks only.\n")
    # ==============

    # SET WORKIND DIR TO SCRIPT DIRECTORY
    SCRIPT_PATH = os.path.abspath(__file__)
    SCRIPT_DIR = os.path.dirname(SCRIPT_PATH) + "/"
    os.chdir(SCRIPT_DIR)
    # ===================================

    MIN_PROXY_FOR_RECHECK = 100
    RECHECK_EVERY_MINS = 30
    CAN_ONLINE_CRAWL = CRWALING_MODULE

    need_Online_Crawl = True
    forceOnlineCrawl = False
    is_ManualFileChanged = False
    countRoutines = 0

    queue_proxies = set()
    set_proxies = set()

    try:
        # FILE "proxies_manual_queue.txt" AGE IN MINUTES
        lastMod = os.path.getmtime(SCRIPT_DIR + "proxies_manual_queue.txt")
        modFileAge = (time() - lastMod) / 60  # FILE AGE IN MINUTES
        is_ManualFileChanged = (
            modFileAge < RECHECK_EVERY_MINS
        )  # IF FILE OLDER THAN RECHECK TIME
    except Exception as e:
        print('MISSING FILES "proxies_manual_queue.txt"\n')

    # IF QUEUE WAS RECENTLY EDITED -> SKIP ONLINE CRAWL
    try:
        # FILE "proxies_queue_unchecked.txt" AGE IN MINUTES
        lastMod = os.path.getmtime(SCRIPT_DIR + "proxies_queue_unchecked.txt")
        modFileAge = (time() - lastMod) / 60  # FILE AGE IN MINUTES
        need_Online_Crawl = not (
            modFileAge < RECHECK_EVERY_MINS / 3
        )  # IF PROXIES WERE RECENTRLY ADDED TO FILE NO NEED TO ONLINE CRAWL
    except Exception as e:
        print('MISSING FILES "proxies_manual_queue.txt"\n')

    # MAIN LOOP: NOT ENOUGH PROXIES -> FULL CRAWL & RESCAN : ELSE -> RESCAN
    while True:
        print("\n[", datetime.now(), "]", "Starting routine...")

        queue_proxies.update(
            gather_queue_proxies.gather_queue_proxies(
                current_queue=set_proxies,
                scan_manual_proxies=is_ManualFileChanged,
                rescan_old_proxies=True,
                collect_queue_history=True,
            )
        )

        # RUN MAIN CRAWL ENGINE IF NEEDED
        if (
            len(set_proxies) < MIN_PROXY_FOR_RECHECK
            and CAN_ONLINE_CRAWL
            and need_Online_Crawl
            or forceOnlineCrawl
        ):
            queue_proxies.update(
                crawl_proxy_services.crawl_online_proxy_services(
                    existing_proxies=queue_proxies
                )
            )
        else:
            print("\n[CRAWLING] No need for online crawling.")
        # ===============================

        # FILTER PROXIES
        # import utils_for_proxies
        # queue_proxies = utils_for_proxies.filter_proxies(queue_proxies)
        # ==============

        # MAIN ENGINE: VALIDATE A PROXY AND ITS ANONIMITY
        if len(queue_proxies):
            print("\nDetecting working proxies and their types, anonymity:")
            set_proxies = detect_proxy_type.detect_proxies_type(
                queue_proxies, save_anonymous=True
            )
        else:
            print("\nNo proxy retrieved for detection.\n")
        # ===============================================

        if set_proxies:
            # SAVE VALIDATED PROXIES TO FILE
            # WORK DIR SET EARLIER TO SCRIPT DIR
            print("\nWriting proxies_.txt")
            with open("proxies_.txt", "w") as f:
                f.writelines("\n".join(set_proxies))
            # ==============================

            # REPLACE FILE TO MAKE MACOS RELOAD LIBERATOR (WATCH FOLDERS SCRIPT MACOS)
            try:
                os.remove("/Users/mbukhman/Downloads/Disbalance Liberator/proxies.txt")
            except OSError:
                pass
            sleep(3)
            try:
                # import shutil
                copyfile(
                    "proxies_.txt",
                    "/Users/mbukhman/Downloads/Disbalance Liberator/proxies.txt",
                    follow_symlinks=True,
                )
            except Exception as e:
                print(
                    "Unable to copy to /Users/mbukhman/Downloads/Disbalance Liberator/proxies.txt",
                    e,
                )
            # ========================================================================

            print("\n", len(set_proxies), "working proxies remained and saved.\n")
        else:
            print("No proxy was detected.")

        countRoutines += 1
        if countRoutines % 4 == 0:
            forceOnlineCrawl = True
        else:
            forceOnlineCrawl = False

        print(
            "Routine done",
            countRoutines,
            "time" if countRoutines == 1 else "times",
            "\n",
        )

        if len(set_proxies) >= MIN_PROXY_FOR_RECHECK:
            # WAITING TIME WITH PROGRESS BAR <- RECHECK_EVERY_MINS
            print("Cool down for", RECHECK_EVERY_MINS, "mins")
            for _ in tqdm.tqdm(
                range(RECHECK_EVERY_MINS), ascii="░ •", unit="m"
            ):  # MINUTES
                sleep(60)  # ONE MINUTE ASLEEP
            print("\n")
            # ====================================================
        else:
            need_Online_Crawl = True
    # =====================================================================
    return 0


if __name__ == "__main__":
    main()
