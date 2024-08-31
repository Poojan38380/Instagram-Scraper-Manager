from modules.accounts import (
    get_all_usernames_and_passwords,
    get_scraping_accounts,
    get_password_by_username,
    select_account_action,
    select_multiple_account_action,
)
from modules.utils import (
    get_random_member,
    check_array_and_proceed,
    print_header,
    print_error,
    print_success,
)
from modules.auth import login
from modules.reels import save_reel, post_reel
import schedule
import time


def post_reel_to_all_accounts():
    print_header("Starting to post reels to all accounts")

    try:
        user_credentials = get_all_usernames_and_passwords()
        if not check_array_and_proceed(user_credentials, "User credentials"):
            return

        for credentials in user_credentials:
            username = credentials["username"]
            password = credentials["password"]

            try:
                scraping_accounts = get_scraping_accounts(username)
                if not check_array_and_proceed(
                    scraping_accounts, f"Scraping accounts for {username}"
                ):
                    continue

                account_to_scrape = get_random_member(scraping_accounts)
                if account_to_scrape is None:
                    print_error(f"No valid scraping account found for {username}")
                    continue

                api = login(username, password)
                if api is None:
                    print_error(f"Failed to login for {username}")
                    continue

                save_reel(username, account_to_scrape)
                post_reel(username, api)

            except Exception as e:
                print_error(f"Error processing credentials for {username}: {str(e)}")

    except Exception as e:
        print_error(f"Failed to process all accounts: {str(e)}")


def post_reel_single_account():
    print_header("Starting to post reel for a single account")

    try:
        username = select_account_action("Select an account to post reel")
        if username is None:
            print_error("No account selected")
            return

        password = get_password_by_username(username)
        if not password:
            print_error(f"No password found for username: {username}")
            return

        scraping_accounts = get_scraping_accounts(username)
        if not check_array_and_proceed(
            scraping_accounts, f"Scraping accounts for {username}"
        ):
            return

        account_to_scrape = get_random_member(scraping_accounts)
        if account_to_scrape is None:
            print_error(f"No valid scraping account found for {username}")
            return

        api = login(username, password)
        if api is None:
            print_error(f"Failed to login for {username}")
            return

        save_reel(username, account_to_scrape)
        post_reel(username, api)

    except Exception as e:
        print_error(f"Failed to post reel for single account: {str(e)}")


def post_reel_multiple_accounts():
    print_header("Starting to post reels for selected accounts")

    try:
        usernames = select_multiple_account_action("Select accounts to post reels")
        if not usernames:
            print_error("No accounts selected")
            return

        for username in usernames:
            password = get_password_by_username(username)
            if not password:
                print_error(f"No password found for username: {username}")
                continue

            scraping_accounts = get_scraping_accounts(username)
            if not check_array_and_proceed(
                scraping_accounts, f"Scraping accounts for {username}"
            ):
                continue

            account_to_scrape = get_random_member(scraping_accounts)
            if account_to_scrape is None:
                print_error(f"No valid scraping account found for {username}")
                continue

            api = login(username, password)
            if api is None:
                print_error(f"Failed to login for {username}")
                continue

            save_reel(username, account_to_scrape)
            post_reel(username, api)
            print_success(f"Reel posted successfully for {username}")

    except Exception as e:
        print_error(f"Failed to post reels for selected accounts: {str(e)}")


def posting_strategy_1():
    # Times converted to IST
    first_time = "14:30"  # 2:30 PM IST
    second_time = "20:30"  # 8:30 PM IST
    third_time = "02:30"  # 2:30 AM IST (next day)

    # Scheduling the job to run at specified times
    schedule.every().day.at(first_time).do(post_reel_to_all_accounts)
    schedule.every().day.at(second_time).do(post_reel_to_all_accounts)
    schedule.every().day.at(third_time).do(post_reel_to_all_accounts)

    print_success(
        f"Posting strategy set up. Reels will be posted at {first_time}, {second_time}, and {third_time} IST daily."
    )

    # Keeping the script running to execute the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)
