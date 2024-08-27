from accounts import get_all_usernames_and_passwords, get_scraping_accounts
from utils import get_random_member


def post_reel_to_all_accounts():
    user_credentials = get_all_usernames_and_passwords()

    for credentials in user_credentials:
        USERNAME = credentials["username"]
        PASSWORD = credentials["password"]
        scraping_accounts = get_scraping_accounts(USERNAME)
        account_to_scrape = get_random_member(scraping_accounts)
        print(account_to_scrape)


post_reel_to_all_accounts()
