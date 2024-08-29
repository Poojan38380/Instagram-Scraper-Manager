import instaloader
import requests
from pathlib import Path
from modules.accounts import (
    is_reel_posted_by_user,
    add_reel_to_user,
    remove_scraping_account_by_username,
    get_scraping_accounts,
)
from modules.utils import (
    delete_file,
    print_header,
    print_error,
    print_success,
    check_array_and_proceed,
    get_random_member,
)
from modules.captions import get_random_caption

# Create an instance of Instaloader
L = instaloader.Instaloader()


def save_reel(username, account_to_scrape):
    print_header(f"Saving reel for user: {username} from account: {account_to_scrape}")
    try:
        profile = instaloader.Profile.from_username(L.context, account_to_scrape)
        reel_directory = Path(f"reels/{username}")
        reel_directory.mkdir(parents=True, exist_ok=True)

        reel_found = False  # To check if any reel is found

        for post in profile.get_posts():
            if post.typename == "GraphVideo" and post.is_video and post.video_url:
                reel_found = True

                if is_reel_posted_by_user(username, post.shortcode):
                    print(f"Reel {post.shortcode} has already been posted.")
                    continue

                print_success(f"\nDownloading Reel: {post.shortcode}")
                try:
                    video_data = requests.get(post.video_url).content
                    video_path = reel_directory / f"{post.shortcode}.mp4"
                    with open(video_path, "wb") as video_file:
                        video_file.write(video_data)
                    print_success(f"Reel {post.shortcode} downloaded successfully.")
                except requests.RequestException as e:
                    print_error(f"Failed to download reel {post.shortcode}: {str(e)}")
                break
            else:
                print(f"Skipping post: {post.shortcode}")

        if not reel_found:
            print_error(
                f"No reels found from the account: {account_to_scrape}. Removing it from scraping accounts from {username}."
            )
            remove_scraping_account_by_username(username, account_to_scrape)
            print(f"Retrying with a new scraping account for user: {username}")
            save_reel(username, get_random_member(get_scraping_accounts(username)))

    except instaloader.exceptions.InstaloaderException as e:
        print_error(f"Failed to load profile {account_to_scrape}: {str(e)}")


def post_reel(username, api):
    print_header(f"Posting reel for user: {username}")
    try:
        reel_folder_path = Path(f"reels/{username}")
        reel_files = list(reel_folder_path.glob("*.mp4"))

        if not check_array_and_proceed(reel_files, "Reel files"):
            return

        for reel_path in reel_files:
            reel_code = reel_path.stem

            # Check if the reel has already been posted
            if is_reel_posted_by_user(username, reel_code):
                print(f"Reel {reel_code} has already been posted. Deleting file.")
                delete_file(reel_path)
                continue

            api.delay_range = [1, 3]

            # Perform the upload using the file path directly
            api.clip_upload(
                path=str(reel_path),
                caption=get_random_caption(),
            )

            print_success(f"Successfully posted reel for {username}")
            add_reel_to_user(username, reel_code)

            thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"

            # Delete the files
            delete_file(thumbnail_path)

            # Exit after posting one reel
            break

    except Exception as e:
        if "feedback_required" in str(e):
            print_error(f"Instagram rate limit hit for {username}.")
            add_reel_to_user(username, reel_code)
            thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"
            delete_file(thumbnail_path)
        else:
            print_error(f"Failed to post reel for {username}: {str(e)}")