import instaloader
import requests

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Login if necessary
# L.login('your_username', 'your_password')

# Specify the username from which you want to download Reels
username = "mortyexplainsit"

# Load the profile
profile = instaloader.Profile.from_username(L.context, username)

# Counter for Reels
reel_count = 0

# Iterate over the posts
for post in profile.get_posts():
    # Check if the post is a Reel (video)
    if post.typename == "GraphVideo" and post.is_video and post.video_url:
        reel_count += 1
        # If this is the second Reel, download the video
        if reel_count == 2:
            print(f"Downloading Reel: {post.shortcode}")
            video_url = post.video_url
            video_data = requests.get(video_url).content
            with open(f"{username}_reel_{post.shortcode}.mp4", "wb") as video_file:
                video_file.write(video_data)
            print(
                f"Reel {post.shortcode} downloaded successfully as {username}_reel_{post.shortcode}.mp4"
            )
            break
    else:
        print(f"Skipping post: {post.shortcode}")
