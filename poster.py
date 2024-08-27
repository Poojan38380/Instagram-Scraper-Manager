from accounts import (
    get_all_usernames_and_passwords,
    get_scraping_accounts,
    add_reel_to_user,
    get_password_by_username,
    select_account_action,
)
from utils import get_random_member, check_array_and_proceed, delete_file
from auth import login
from reels import save_reel
from captions import get_random_caption
from pathlib import Path
import time


def poster_function(username, api):
    # Define the path to the folder containing the reel
    reel_folder_path = Path(f"reels/{username}")

    # Get the mp4 file in the folder
    reel_files = list(reel_folder_path.glob("*.mp4"))

    if not reel_files:
        print(f"No reel found for {username} in {reel_folder_path}")
        return

    # Since there should be only one reel, pick the first one
    reel_path = reel_files[0]
    # Extract the reel code (filename without extension)
    reel_code = reel_path.stem

    # Post the reel to Instagram
    try:
        api.delay_range = [1, 3]

        # Ensure posting the reel completes before proceeding
        api.clip_upload(
            path=reel_path,
            caption=get_random_caption(),
        )

        print(f"Successfully posted reel for {username}")
        add_reel_to_user(username, reel_code)

        # Define the path to the thumbnail (assumed to be reel_path.jpg)
        thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"

        # Retry file deletion if access is denied
        for _ in range(5):
            try:
                delete_file(reel_path)  # Attempt to delete the video file
                delete_file(thumbnail_path)  # Delete the thumbnail
                break
            except Exception as e:
                print(f"Retrying deletion in 2 seconds due to error: {e}")
                time.sleep(2)

    except Exception as e:
        if "feedback_required" in str(e):
            print(f"Instagram rate limit hit for {username}.")
            add_reel_to_user(username, reel_code)

            # Define the path to the thumbnail (assumed to be reel_path.jpg)
            thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"
            # Retry file deletion if access is denied
            for _ in range(5):
                try:
                    delete_file(reel_path)  # Attempt to delete the video file
                    delete_file(thumbnail_path)  # Delete the thumbnail
                    break
                except Exception as e:
                    print(f"Retrying deletion in 2 seconds due to error: {e}")
                    time.sleep(2)
        else:
            print(f"Failed to post reel for {username}: {str(e)}")


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
            continue
        account_to_scrape = get_random_member(scraping_accounts)

        api = login(USERNAME, PASSWORD)
        save_reel(USERNAME, account_to_scrape)
        poster_function(USERNAME, api)


def post_reel_single_account():
    username = select_account_action("Select an account to post reel")
    password = get_password_by_username(username)
    scraping_accounts = get_scraping_accounts(username)
    if not check_array_and_proceed(
        scraping_accounts, f"scraping_accounts for {username} "
    ):
        return
    account_to_scrape = get_random_member(scraping_accounts)
    api = login(username, password)
    save_reel(username, account_to_scrape)
    poster_function(username, api)
