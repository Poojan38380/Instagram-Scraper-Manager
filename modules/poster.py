from modules.accounts import (
    get_all_usernames_and_passwords,
    get_scraping_accounts,
    get_password_by_username,
    select_account_action,
    select_multiple_account_action,
    tagline_by_username,
)
from modules.utils import (
    get_random_member,
    check_array_and_proceed,
    print_header,
    print_error,
    print_success,
)
from modules.auth import login
from modules.reels import delete_reel, save_reel, post_reel
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
                api = login(username, password)
                if api is None:
                    print_error(f"Failed to login for {username}")
                    continue

                # Try to post reel
                print(f"Flushing: {username}")
                reel_posted = post_reel(username, api)
                if reel_posted == "no_reels_left":

                    tagline = tagline_by_username(username)
                    scraping_accounts = get_scraping_accounts(username)
                    if not check_array_and_proceed(
                        scraping_accounts, f"Scraping accounts for {username}"
                    ):
                        continue
                    account_to_scrape = get_random_member(scraping_accounts)
                    if account_to_scrape is None:
                        print_error(f"No valid scraping account found for {username}")
                        continue
                    save_reel(username, account_to_scrape, tagline)  # type: ignore

                    print_header(f"Posting reel for user: {username}")
                    # Retry posting after saving new reels
                    reel_posted = post_reel(username, api)
                    if not reel_posted:
                        print_error(f"Failed to post a reel for {username} ")
                    else:
                        print_success(f"Successfully posted reel for {username}")

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
        tagline = tagline_by_username(username)

        api = login(username, password)
        if api is None:
            print_error(f"Failed to login for {username}")
            return

        # Try to post reel
        print(f"Flushing: {username}")
        reel_posted = post_reel(username, api)

        # If posting failed because no reel was available, save reels and retry posting
        if reel_posted == "no_reels_left":
            print(f"No reels found for {username}, attempting to save new reels.")
            scraping_accounts = get_scraping_accounts(username)
            if not check_array_and_proceed(
                scraping_accounts, f"Scraping accounts for {username}"
            ):
                return

            account_to_scrape = get_random_member(scraping_accounts)
            if account_to_scrape is None:
                print_error(f"No valid scraping account found for {username}")
                return
            save_reel(username, account_to_scrape, tagline)  # type: ignore

            print_header(f"Posting reel for user: {username}")
            # Retry posting after saving new reels
            reel_posted = post_reel(username, api)
            if not reel_posted:
                print_error(f"Failed to post a reel for {username} ")
            else:
                print_success(f"Successfully posted reel for {username}")

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
            tagline = tagline_by_username(username)
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
 
            save_reel(username, account_to_scrape, tagline)  # type: ignore
            post_reel(username, api)
            print_success(f"Reel posted successfully for {username}")

    except Exception as e:
        print_error(f"Failed to post reels for selected accounts: {str(e)}")


def posting_strategy_1():
    first_time = "07:00"  # Morning post at 7 AM
    second_time = "12:30"  # Afternoon post at 12:30 PM
    third_time = "19:00"  # Evening post at 7 PM

    # Scheduling the job to run at specified times
    schedule.every().day.at(first_time).do(post_reel_to_all_accounts)
    schedule.every().day.at(second_time).do(post_reel_to_all_accounts)
    schedule.every().day.at(third_time).do(post_reel_to_all_accounts)

    print_success(
        f"Posting strategy set up. Reels will be posted at {first_time}, {second_time}, and {third_time} local time daily."
    )

    # Keeping the script running to execute the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)


def post_reel_multiple_times_for_account():
    print_header("Starting to post reels multiple times for a single account")

    try:
        # Step 1: User selects an account
        username = select_account_action("Select an account to post reel")
        if username is None:
            print_error("No account selected")
            return

        # Step 2: Get the password and tagline for the selected account
        password = get_password_by_username(username)
        if not password:
            print_error(f"No password found for username: {username}")
            return
        tagline = tagline_by_username(username)

        # Step 3: Prompt the user for how many times to post
        try:
            num_posts = int(
                input(f"Enter the number of times to post reels for {username}: ")
            )
            if num_posts <= 0:
                print_error("The number of posts must be greater than zero.")
                return
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")
            return

        # Step 4: Log in to the account
        api = login(username, password)
        if api is None:
            print_error(f"Failed to login for {username}")
            return

        # Step 5: Post the reel `X` times
        for i in range(num_posts):
            print(f"Flushing: {username} - Attempt {i+1} of {num_posts}")

            reel_posted = post_reel(username, api)

            # If no reels are left, scrape new reels and retry
            if reel_posted == "no_reels_left":
                print(f"No reels found for {username}, attempting to save new reels.")
                scraping_accounts = get_scraping_accounts(username)
                if not check_array_and_proceed(
                    scraping_accounts, f"Scraping accounts for {username}"
                ):
                    break

                account_to_scrape = get_random_member(scraping_accounts)
                if account_to_scrape is None:
                    print_error(f"No valid scraping account found for {username}")
                    break
                save_reel(username, account_to_scrape, tagline) # type: ignore

                print_header(f"Posting reel for user: {username}")
                reel_posted = post_reel(username, api)

            if not reel_posted:
                print_error(f"Failed to post reel {i+1} for {username}")
            else:
                print_success(f"Successfully posted reel {i+1} for {username}")

    except Exception as e:
        print_error(f"Failed to post reels multiple times for {username}: {str(e)}")


def single_account_flush():
    print_header("Flushing single account")

    try:
        username = select_account_action("Select an account to flush")
        if username is None:
            print_error("No account selected")
            return

        password = get_password_by_username(username)
        if not password:
            print_error(f"No password found for username: {username}")
            return

        api = login(username, password)
        if api is None:
            print_error(f"Failed to login for {username}")
            return

        post_reel(username, api)

    except Exception as e:
        print_error(f"Failed to flush single account: {str(e)}")


def all_accounts_flush():
    print_header("Flushing all accounts")

    try:
        user_credentials = get_all_usernames_and_passwords()
        if not check_array_and_proceed(user_credentials, "User credentials"):
            return

        for credentials in user_credentials:
            username = credentials["username"]
            password = credentials["password"]

            try:

                api = login(username, password)
                if api is None:
                    print_error(f"Failed to login for {username}")
                    continue

                post_reel(username, api)

            except Exception as e:
                print_error(f"Error processing credentials for {username}: {str(e)}")

    except Exception as e:
        print_error(f"Failed to process all accounts: {str(e)}")


def delete_reel_for_selected_account():
    print_header("Deleting reel for selected account")

    try:
        username = select_account_action("Select an account to delete reel")
        if username is None:
            print_error("No account selected")
            return

        password = get_password_by_username(username)
        if not password:
            print_error(f"No password found for username: {username}")
            return

        api = login(username, password)
        if api is None:
            print_error(f"Failed to login for {username}")
            return

        delete_reel(api)
        print_success(f"Reel deleted successfully for {username}")

    except Exception as e:
        print_error(f"Failed to delete reel for selected account: {str(e)}")
