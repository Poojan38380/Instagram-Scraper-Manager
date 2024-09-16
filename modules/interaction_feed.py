from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.accounts import (
    get_all_usernames_and_passwords,
    get_keywords_by_username,
    get_password_by_username,
    select_account_action,
)
from modules.activity import human_like_scrolling
from modules.auth import login
from modules.utils import print_error, print_header, print_success


def explore_feed_for_single():
    # Step 1: Ask the user to choose an account from the database
    selected_username = select_account_action(
        "Select an account to scroll through its feed:"
    )
    if not selected_username:
        return  # Exit if no valid account is selected

    # Step 2: Retrieve the account's password from the database
    password = get_password_by_username(selected_username)
    if not password:
        return  # Exit if the password retrieval fails

    # Step 3: Login to the selected account using the retrieved credentials
    api = login(selected_username, password)
    if api is None:
        print_error("Failed to login. Check your credentials and try again.")
        return  # Exit if login fails
    keywords = get_keywords_by_username(selected_username)

    # Step 4: Pass the logged-in api object to the human_like_scrolling function
    try:
        human_like_scrolling(
            api, username=selected_username, keywords=keywords
        )  # Customize max_posts and action_probability as needed
    except Exception as e:
        print_error(f"An error occurred during scrolling: {e}")


def explore_feed_single_account(account):
    username = account["username"]
    password = account["password"]

    # Step 1: Login to the account using the credentials
    print_header(f"Logging in to {username}...")
    api = login(username, password)
    keywords = get_keywords_by_username(username)

    if api is None:
        print_error(f"Failed to login to '{username}'. Skipping.")
        return False  # Skip if login fails

    # Step 2: Pass the logged-in api object to the human_like_scrolling function
    try:
        print(f"Scrolling through feed for '{username}'...")
        human_like_scrolling(
            api, username=username, keywords=keywords, total_time=1800
        )  # Customize max_posts and action_probability as needed
    except Exception as e:
        print_error(f"An error occurred during scrolling for '{username}': {e}")
        return False
    else:
        print_success(f"Successfully scrolled through feed for '{username}'.")
        return True


def explore_feed_all_accounts():
    # Step 1: Get all usernames and passwords from the database
    all_accounts = get_all_usernames_and_passwords()

    if not all_accounts:
        print_error("No accounts found in the database.")
        return  # Exit if no accounts are found

    # Step 2: Set up a ThreadPoolExecutor to run multiple accounts concurrently
    max_workers = min(25, len(all_accounts))  # Adjust max_workers as needed
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Step 3: Submit tasks for each account to the executor
        futures = {
            executor.submit(explore_feed_single_account, account): account["username"]
            for account in all_accounts
        }

        # Step 4: Process the results as they complete
        for future in as_completed(futures):
            username = futures[future]
            try:
                result = future.result()
                if result:
                    print_success(f"Scrolling completed for '{username}'.")
                else:
                    print_error(f"Scrolling failed for '{username}'.")
            except Exception as e:
                print_error(f"An error occurred for '{username}': {e}")

    print_header("Finished scrolling through all accounts.")
