def main(force_online_crawl: bool = False, minimum_proxy_for_recheck: int = 70, clear_queue=False) -> int:
    """
    MAIN FUNCTION
    """
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

    # SELENIUM AND WEB_DRIVER UPDATE
    try:
        import selenium
        import webdriver_manager
    except Exception as e:
        print("Run: python -m pip install selenium webdriver-manager")
        return -1
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        # By default, all driver binaries are saved to user.home/.wdm folder.
        # You can override this setting and save binaries to project.root/.wdm.
        os.environ["WDM_LOCAL"] = "1"
        ChromeDriverManager(path="./chromedriver").install()
    except Exception as e:
        print("Error occurred while updating webdriver-manager", e)
        return -1
    # ==============================

    # DETECTING PROXIES ENGINE
    try:
        import gather_queue_proxies
    except Exception:
        print("Missing main gathering module 'gather_queue_proxies.py'.")
        return -1
    # ========================
    # DETECTING PROXIES ENGINE
    try:
        import detect_proxy_type
    except Exception:
        print("Missing main proxy detection module 'detect_proxy_type.py'.")
        return -1
    # ========================

    # CRAWLING MODULE
    try:
        import crawl_proxy_services

        CRAWLING_MODULE = True
    except Exception as e:
        CRAWLING_MODULE = False
        print("Missing crawling module. Manual checks and rechecks only.\n")
    # ==============

    # SET WORKING DIR TO SCRIPT DIRECTORY
    SCRIPT_PATH = os.path.abspath(__file__)
    SCRIPT_DIR = os.path.dirname(SCRIPT_PATH) + "/"
    os.chdir(SCRIPT_DIR)
    # ===================================

    MINIMUM_PROXY_FOR_RECHECK = minimum_proxy_for_recheck
    RECHECK_EVERY_MINS = 60
    CAN_ONLINE_CRAWL = CRAWLING_MODULE

    need_online_crawl = True
    force_online_crawl = force_online_crawl
    is_manual_file_changed = False
    count_routines = 0

    queue_proxies = set()
    set_proxies = set()

    # IF QUEUE WAS RECENTLY EDITED -> SKIP ONLINE CRAWL
    try:
        # FILE "proxies_queue_unchecked.txt" AGE IN MINUTES
        lastMod = os.path.getmtime(SCRIPT_DIR + "proxies_queue_unchecked.txt")
        modified_file_age = (time() - lastMod) / 60  # FILE AGE IN MINUTES
        need_online_crawl = not (
            modified_file_age < RECHECK_EVERY_MINS / 3
        )  # IF PROXIES WERE RECENTLY ADDED TO FILE NO NEED TO ONLINE CRAWL
    except Exception as e:
        print('MISSING FILES "proxies_queue_unchecked.txt"\n')

    # CLEAR UNCHECKED QUEUE
    if clear_queue:
        try:
            open(SCRIPT_DIR + "proxies_queue_unchecked.txt", 'w').close()
        except:
            print('Can\'t access file "proxies_queue_unchecked.txt"\n')


    # MAIN LOOP:
    # NOT ENOUGH PROXIES -> FULL CRAWL & RESCAN : ELSE -> RESCAN
    while True:

        try:
            # FILE "proxies_manual_queue.txt" AGE IN MINUTES
            lastMod = os.path.getmtime(SCRIPT_DIR + "proxies_manual_queue.txt")
            modified_file_age = (time() - lastMod) / 60  # FILE AGE IN MINUTES
            is_manual_file_changed = (
                modified_file_age < RECHECK_EVERY_MINS
            )  # IF FILE OLDER THAN RECHECK TIME
        except Exception as e:
            print('MISSING FILES "proxies_manual_queue.txt"\n')

        print("\n[", datetime.now(), "]", "Starting routine...")

        queue_proxies.update(
            gather_queue_proxies.gather_queue_proxies(
                current_queue=set_proxies,
                collect_queue_history=True,
                scan_manual_proxies=is_manual_file_changed,
                collect_checked_proxies=True,
                save_queue_file=False,
            )
        )

        # KILL TERMINAL PROCESS TO SAVE INTERNET FOR CRAWLING AND DETECTING
        from subprocess import call

        call(["osascript", "-e", 'tell application "Terminal" to quit'])
        # =================================================================

        # RUN MAIN CRAWL ENGINE IF NEEDED
        if CAN_ONLINE_CRAWL and (force_online_crawl or need_online_crawl):
            queue_proxies = crawl_proxy_services.crawl_online_proxy_services(
                existing_proxies=queue_proxies,
                save_queue_file=True,
            )
            force_online_crawl = False
        else:
            print("\n[CRAWLING] No need for online crawling.")
        # ===============================

        # FILTER PROXIES
        # import utils_for_proxies
        # queue_proxies = utils_for_proxies.filter_proxies(queue_proxies)
        # ==============

        # VALIDATE A PROXY AND ITS ANONIMITY
        if len(queue_proxies):
            print("\nDetecting working proxies and their types, anonymity:")
            set_proxies = detect_proxy_type.detect_proxies_type(
                queue_proxies,
                save_anonymous=True,
                concurrect_checks=50,
            )
        else:
            print("\nNo proxy retrieved for detection.\n")
        # ==================================

        if set_proxies:
            # SAVE VALIDATED PROXIES TO FILE
            # WORK DIR SET EARLIER TO SCRIPT DIR
            try:
                with open("proxies_.txt", "w") as f:
                    f.writelines("\n".join(set_proxies))
                print("\nWriting", len(set_proxies), "working proxies to proxies_.txt")
            except Exception as e:
                print("Couldn't write to proxies_.txt", e)
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
        else:
            print("No proxy was detected.")

        count_routines += 1

        # FORCE ONLINE CRAWL EVERY 4 ROUTINES
        if count_routines % 5 == 0:
            force_online_crawl = True
        else:
            force_online_crawl = False
        # ===================================

        # END ROUTINE MESSAGE
        print(
            "[",
            datetime.now(),
            "]",
            "Routine done",
            count_routines,
            "time" if count_routines == 1 else "times",
            "\n",
        )
        # ===================

        if len(set_proxies) >= MINIMUM_PROXY_FOR_RECHECK:
            # WAITING TIME WITH PROGRESS BAR <- RECHECK_EVERY_MINS
            print("Cool down for", RECHECK_EVERY_MINS, "mins")
            for _ in tqdm.tqdm(
                range(RECHECK_EVERY_MINS), ascii="░ •", unit="m"
            ):  # MINUTES
                sleep(60)  # ONE MINUTE ASLEEP
            print("\n")
            need_online_crawl = False
            # ====================================================
        else:
            need_online_crawl = True
    # ==========================================================
    # ==========
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Crawl and parse proxies. By mbukhman.")
    parser.add_argument('--force', '-f', help='force full crawl with the first run', default=False, action="store_true")
    parser.add_argument('--min-proxies', '-mp', type=int, metavar='n', help='minimum proxies count (n) to restart crawling immediately (default 70)', default=70)
    parser.add_argument('--clean-start', '-cls', help='clean unchecked queue left from previous runs', default=False, action="store_true")
    args = parser.parse_args()

    if args.force:
        force_online_crawl = True
        print("Forcing first crawl (--force)")
    else:
        force_online_crawl = False

    if args.min_proxies:
        minimum_proxy_for_recheck = args.min_proxies
        print("Limiting minimum proxies count by", minimum_proxy_for_recheck)
    else:
        minimum_proxy_for_recheck = 70

    if args.clean_start:
        clear_queue = True
        print("Clearing unchecked queue in proxies_queue_unchecked.txt")
    else:
        clear_queue = False

    main(force_online_crawl=force_online_crawl, minimum_proxy_for_recheck=minimum_proxy_for_recheck, clear_queue=clear_queue)
