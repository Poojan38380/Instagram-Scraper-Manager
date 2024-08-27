import instaloader
import requests
import os
from accounts import is_reel_posted_by_user

# Create an instance of Instaloader
L = instaloader.Instaloader()


def save_reel(username, account_to_scrape):
    # Load the profile
    profile = instaloader.Profile.from_username(L.context, account_to_scrape)

    # Create the directory if it doesn't exist
    os.makedirs(f"reels/{username}", exist_ok=True)

    # Iterate over the posts
    for post in profile.get_posts():
        # Check if the post is a Reel (video)
        if post.typename == "GraphVideo" and post.is_video and post.video_url:

            # Check if the reel is already posted
            if is_reel_posted_by_user(username, post.shortcode):
                print(f"Reel {post.shortcode} has already been posted.")
                continue

            print(f"Downloading Reel: {post.shortcode}")
            video_url = post.video_url
            video_data = requests.get(video_url).content
            with open(f"reels/{username}/{post.shortcode}.mp4", "wb") as video_file:
                video_file.write(video_data)
            print(
                f"Reel {post.shortcode} downloaded successfully as {post.shortcode}.mp4"
            )
            break
        else:
            print(f"Skipping post: {post.shortcode}")
