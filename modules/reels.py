import random
import time
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
                try:
                    delete_file(reel_path)
                except PermissionError as e:
                    if "WinError 32" in str(e):
                        print_error(
                            f"File in use error: {str(e)}. Returning no reels left."
                        )
                        return (
                            "no_reels_left"  # If file is in use, return no_reels_left
                        )

                # Recheck if the folder is empty after deletion
                if not any(reel_folder_path.glob("*.mp4")):
                    return "no_reels_left"  # Folder is empty after deletion
                continue

            api.delay_range = [1, 3]

            # Get captions
            CAPTION = generate_caption(username)
            # LOCATION = get_instagram_location(api)

            # Perform the upload using the file path directly
            media = api.clip_upload(
                path=str(reel_path),
                caption=CAPTION,
                # location=LOCATION,
                extra_data={
                    "custom_accessibility_caption": CAPTION,
                    "share_to_feed": False,  # Do not share the reel to the main feed
                },
            )

            print_success(f"Successfully posted reel for {username}\n\n")
            add_reel_to_user(username, reel_code)

            print(f"Initializing posting story...")
            post_to_story(api, media, reel_path, username, reel_folder_path)

            # View and Like the posted reel
            try:
                api.media_like(media.id)
                print_success(f"Reel {reel_code} liked successfully.")
            except Exception as e:
                print_error(f"Failed to like reel {reel_code}: {str(e)}")

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
            thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"  # type: ignore
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


# def delete_reels_below_view_count(api, username, view_threshold):
#     """
#     Delete reels that have fewer views than the specified threshold, ignoring the first 9 posts.

#     :param api: Instagram API instance.
#     :param username: The username of the profile to check reels for.
#     :param view_threshold: The minimum view count required for a reel to be kept.
#     """
#     try:
#         print_header(f"Deleting reels below {view_threshold} views for {username}")

#         profile = instaloader.Profile.from_username(L.context, username)

#         post_count = 0  # Counter to keep track of posts

#         for post in profile.get_posts():
#             post_count += 1

#             # Skip the first 9 posts
#             if post_count <= 9:
#                 print(f"Skipping post {post_count}: {post.shortcode}")
#                 continue

#             if post.typename == "GraphVideo" and post.is_video:
#                 reel_views = post.video_view_count  # Get view count for the reel
#                 reel_code = post.shortcode

#                 # Check if the view count is below the threshold
#                 if reel_views < view_threshold:
#                     try:
#                         print_success(
#                             f"Reel {reel_code} has {reel_views} views, below threshold. Deleting..."
#                         )

#                         # Convert reel code to media PK and delete the reel
#                         reel_pk = api.media_pk_from_code(reel_code)
#                         api.media_delete(reel_pk)

#                         print_success(f"Reel {reel_code} deleted successfully.")
#                     except Exception as e:
#                         print_error(f"Failed to delete reel {reel_code}: {str(e)}")
#                 else:
#                     print(f"Reel {reel_code} has {reel_views} views. Keeping it.")

#     except instaloader.exceptions.InstaloaderException as e:
#         print_error(f"Failed to load profile {username}: {str(e)}")
#     except Exception as e:
#         print_error(f"An unexpected error occurred: {str(e)}")


def delete_low_performing_reels(api, username, reels_to_keep=15):
    """
    Delete reels that have fewer views than the minimum view count of the top reels_to_keep reels.

    :param api: Instagram API instance.
    :param username: The username of the profile to check reels for.
    :param reels_to_keep: Number of top-performing reels to keep.
    """
    try:
        print_header(
            f"Deleting reels below top {reels_to_keep} view count for {username}"
        )

        profile = instaloader.Profile.from_username(L.context, username)

        # Fetch reels and their view counts
        reels_with_views = []
        for post in profile.get_posts():
            if post.typename == "GraphVideo" and post.is_video:
                reels_with_views.append(
                    {"shortcode": post.shortcode, "view_count": post.video_view_count}
                )

        # Check if we have enough reels to compare
        if len(reels_with_views) < reels_to_keep:
            print_error(
                f"User {username} has fewer than {reels_to_keep} reels. Cannot proceed."
            )
            return

        # Sort reels by view count in descending order
        reels_with_views.sort(key=lambda x: x["view_count"], reverse=True)

        # Get the top reels_to_keep reels
        top_reels = reels_with_views[:reels_to_keep]

        # Extract the minimum view count from the top reels_to_keep reels
        min_top_views = min([reel["view_count"] for reel in top_reels])
        print_success(
            f"Minimum view count of top {reels_to_keep} reels: {min_top_views} views"
        )

        # Iterate through all posts to delete reels with view count less than the minimum of top reels_to_keep
        post_count = 0  # Counter to keep track of posts
        for post in profile.get_posts():
            post_count += 1

            if post.typename == "GraphVideo" and post.is_video:
                reel_views = post.video_view_count  # Get view count for the reel
                reel_code = post.shortcode

                # Delete reels below the minimum view count of top reels_to_keep
                if reel_views < min_top_views:
                    try:
                        print(
                            f"Reel {reel_code} has {reel_views} views, below threshold. Deleting..."
                        )

                        # Random sleep to avoid bot detection
                        sleep_duration = random.uniform(2, 6)
                        print(
                            f"Waiting for {sleep_duration:.2f} seconds before deleting..."
                        )
                        time.sleep(sleep_duration)

                        # Convert reel code to media PK and delete the reel
                        reel_pk = api.media_pk_from_code(reel_code)
                        api.media_delete(reel_pk)

                        print_success(f"Reel {reel_code} deleted successfully.")
                    except Exception as e:
                        print_error(f"Failed to delete reel {reel_code}: {str(e)}")
                else:
                    print(f"Reel {reel_code} has {reel_views} views. Keeping it.")

    except instaloader.exceptions.InstaloaderException as e:
        print_error(f"Failed to load profile {username}: {str(e)}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
