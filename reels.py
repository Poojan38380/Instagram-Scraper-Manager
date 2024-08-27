import os
import time
import instaloader
import requests
from pathlib import Path
from accounts import is_reel_posted_by_user, add_reel_to_user
from utils import (
    delete_file,
    print_header,
    print_error,
    print_success,
    check_array_and_proceed,
)
from captions import get_random_caption

# Create an instance of Instaloader
L = instaloader.Instaloader()


def save_reel(username, account_to_scrape):
    print_header(f"Saving reel for user: {username} from account: {account_to_scrape}")
    try:
        profile = instaloader.Profile.from_username(L.context, account_to_scrape)
        reel_directory = Path(f"reels/{username}")
        reel_directory.mkdir(parents=True, exist_ok=True)

        for post in profile.get_posts():
            if post.typename == "GraphVideo" and post.is_video and post.video_url:
                if is_reel_posted_by_user(username, post.shortcode):
                    print_error(f"Reel {post.shortcode} has already been posted.")
                    continue

                print_success(f"Downloading Reel: {post.shortcode}")
                try:
                    video_data = requests.get(post.video_url).content
                    with open(
                        reel_directory / f"{post.shortcode}.mp4", "wb"
                    ) as video_file:
                        video_file.write(video_data)
                    print_success(f"Reel {post.shortcode} downloaded successfully.")
                except requests.RequestException as e:
                    print_error(f"Failed to download reel {post.shortcode}: {str(e)}")
                break
            else:
                print_error(f"Skipping post: {post.shortcode}")
    except instaloader.exceptions.InstaloaderException as e:
        print_error(f"Failed to load profile {account_to_scrape}: {str(e)}")


def post_reel(username, api):
    print_header(f"Posting reel for user: {username}")
    try:
        reel_folder_path = Path(f"reels/{username}")
        reel_files = list(reel_folder_path.glob("*.mp4"))

        if not check_array_and_proceed(reel_files, "Reel files"):
            return

        reel_path = reel_files[0]
        reel_code = reel_path.stem

        api.delay_range = [1, 3]
        api.clip_upload(
            path=reel_path,
            caption=get_random_caption(),
        )

        print_success(f"Successfully posted reel for {username}")
        add_reel_to_user(username, reel_code)

        thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"

        # Adding a delay before attempting to delete the files
        time.sleep(2)
        delete_file(thumbnail_path)
        delete_file(reel_path)

    except Exception as e:
        if "feedback_required" in str(e):
            print_error(f"Instagram rate limit hit for {username}.")
            add_reel_to_user(username, reel_code)
            thumbnail_path = reel_folder_path / f"{reel_code}.mp4.jpg"
            delete_file(thumbnail_path)
            delete_file(reel_path)
        else:
            print_error(f"Failed to post reel for {username}: {str(e)}")
