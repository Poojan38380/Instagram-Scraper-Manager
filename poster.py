from accounts import (
    get_all_usernames_and_passwords,
    get_scraping_accounts,
    get_password_by_username,
    select_account_action,
)
from utils import (
    get_random_member,
    check_array_and_proceed,
    print_header,
    print_error,
    print_success,
)
from auth import login
from reels import save_reel, post_reel


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
