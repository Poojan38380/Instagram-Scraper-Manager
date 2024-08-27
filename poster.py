from accounts import get_all_usernames_and_passwords, get_scraping_accounts
from utils import get_random_member, check_array_and_proceed
from auth import login


def post_reel_to_all_accounts():
    user_credentials = get_all_usernames_and_passwords()
    if not check_array_and_proceed(user_credentials, "User credentials"):
        return

    for credentials in user_credentials:
        USERNAME = credentials["username"]
        PASSWORD = credentials["password"]
        scraping_accounts = get_scraping_accounts(USERNAME)
        if not check_array_and_proceed(
            scraping_accounts, f"scraping_accounts for {USERNAME} "
        ):
            return
        account_to_scrape = get_random_member(scraping_accounts)

        api = login(USERNAME, PASSWORD)


post_reel_to_all_accounts()
