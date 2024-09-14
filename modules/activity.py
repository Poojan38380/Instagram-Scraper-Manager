import random
import time
import json


def human_like_scrolling(api, max_posts=10, action_probability=0.5):
    """
    Scrolls through the Instagram newsfeed or reelfeed and interacts with posts like a human.

    Args:
        api (Client): The instagrapi API client object.
        max_posts (int): Maximum number of posts to interact with. Default is 10.
        action_probability (float): Probability (0 to 1) of liking a post or viewing a reel. Default is 0.5.
    """

    try:
        # Fetch the newsfeed/reelfeed posts
        feed = api.get_timeline_feed()  # For newsfeed
        # feed = api.reels_tray()   # For reel feed

        if not feed:
            print("No posts found in the feed.")
            return

        print(f"Retrieved {len(feed)} posts from the feed.")

        # Save the feed to a JSON file
        with open("feed_data.json", "w") as json_file:
            json.dump(feed, json_file, indent=4)
        print("Feed saved to feed_data.json")

        interacted_posts = 0

        print(f"Finished interacting with {interacted_posts} posts.")

    except Exception as e:
        print(f"An error occurred while scrolling: {str(e)}")
