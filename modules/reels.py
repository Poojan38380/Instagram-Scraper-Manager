import instaloader
import requests
from pathlib import Path
from modules.accounts import (
    is_reel_posted_by_user,
    add_reel_to_user,
    remove_scraping_account_by_username,
    get_scraping_accounts,
)
from modules.misc import get_instagram_location
from modules.utils import (
    delete_file,
    get_user_input,
    print_header,
    print_error,
    print_success,
    check_array_and_proceed,
    get_random_member,
)
from modules.captions import generate_caption
from modules.story import post_to_story
from modules.video import add_margins_to_reel

# Create an instance of Instaloader
L = instaloader.Instaloader()


def save_reel(username, account_to_scrape, tagline=""):
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
                # Added a feature to filter out posts that have certain view_count threshold
                # if not should_save_reel(post):
                #     continue

                print_success(f"\nDownloading Reel: {post.shortcode}")
                try:
                    video_data = requests.get(post.video_url).content
                    video_path = reel_directory / f"{post.shortcode}_raw.mp4"
                    with open(video_path, "wb") as video_file:
                        video_file.write(video_data)
                    print_success(f"Reel {post.shortcode}_raw downloaded successfully.")
                    add_margins_to_reel(video_path, top_text=tagline)
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

        # Check if there are any reel files to post
        if not check_array_and_proceed(reel_files, "Reel files"):
            return "no_reels_left"  # Indicate that no reels were posted due to empty folder

        for reel_path in reel_files:
            reel_code = reel_path.stem

            # Check if the reel has already been posted
            if is_reel_posted_by_user(username, reel_code):
                print(f"Reel {reel_code} has already been posted. Deleting file.")
                delete_file(reel_path)

                # Recheck if the folder is empty after deletion
                if not any(reel_folder_path.glob("*.mp4")):
                    return "no_reels_left"  # Folder is empty after deletion
                continue

            api.delay_range = [1, 3]

            # Get captions
            CAPTION = generate_caption(username)
            LOCATION = get_instagram_location(api)

            # Perform the upload using the file path directly
            media = api.clip_upload(
                path=str(reel_path),
                caption=CAPTION,
                location=LOCATION,
                extra_data={
                    "custom_accessibility_caption": CAPTION,
                },
            )

            print_success(f"Successfully posted reel for {username}")
            add_reel_to_user(username, reel_code)

            print(f"Initializing posting story...")
            post_to_story(api, media, reel_path, username, reel_folder_path)

            # Exit after posting one reel
            return "reel_posted"  # Indicate that reel posting was successful

    except Exception as e:
        if "feedback_required" in str(e):
            print_error(f"Instagram rate limit hit for {username}.")
            add_reel_to_user(username, reel_code)
        else:
            print_error(f"Failed to post reel for {username}: {str(e)}")
        return "posting_error"  # Indicate that reel posting failed
    finally:
        # Clean up the uploaded video file if it exists, only if reel_code is defined
        if "reel_code" in locals():
            thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"
            delete_file(thumbnail_path)


def delete_reel(api):
    try:
        # Get reel code from user input
        reel_code = get_user_input("Enter the reel code")

        if not reel_code:
            print_error("Reel code cannot be empty.")
            return

        try:
            # Convert reel code to media PK
            reel_pk = api.media_pk_from_code(reel_code)
        except Exception as e:
            print_error(
                f"Failed to retrieve media PK from reel code '{reel_code}': {str(e)}"
            )
            return

        try:
            # Attempt to delete the reel
            api.media_delete(reel_pk)
            print_success(f"Reel '{reel_code}' deleted successfully.")
        except Exception as e:
            if "feedback_required" in str(e):
                print_error(
                    f"Instagram rate limit hit. Unable to delete reel '{reel_code}' at this time."
                )
            else:
                print_error(f"Failed to delete reel '{reel_code}': {str(e)}")

    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
