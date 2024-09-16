import random
import time
import json
from modules.utils import print_error

comments = ["Nice post!", "Awesome!", "Great content!", "Love this!", "❤️❤️"]


def human_like_scrolling(
    api,
    username="",
    total_time=60,
    action_probability=0.4,
    keyword_action_boost=2,  # Additional boost for actions when keywords are found
    comments_list=comments,
    keywords=None,
):
    """
    Scrolls through the Instagram newsfeed or reel feed and interacts with posts in a human-like manner for a specified duration.
    Interacts with posts based on specific keywords in the caption if provided, with increased probability of liking/commenting.

    Args:
        api (Client): The instagrapi API client object.
        total_time (int): Total time to spend scrolling in seconds. Default is 60 seconds.
        action_probability (float): Base probability (0 to 1) of liking a post or viewing a reel. Default is 0.5.
        keyword_action_boost (float): Additional boost to action probability when keywords are found in the caption. Default is 0.3.
        comments_list (list): List of comments to randomly choose from when commenting. Default is None.
        keywords (list): List of keywords to check in the caption text. Default is None.
    """

    start_time = time.time()  # Record the starting time
    interacted_posts = 0

    # If no keywords are provided, use an empty list
    if keywords is None:
        keywords = []

    try:
        while (time.time() - start_time) < total_time:
            # Fetch the newsfeed/reel feed posts
            feed = api.get_timeline_feed()  # For newsfeed
            # feed = api.reels_tray()  # For reel feed

            if not feed or "feed_items" not in feed:
                print_error(f"{username} : No posts found.")
                return

            # Filter out only media posts and ignore suggested users
            posts = [
                item["media_or_ad"]
                for item in feed["feed_items"]
                if "media_or_ad" in item
            ]
            print(f"{username} : Retrieved {len(posts)} posts.")

            # If no posts are left, exit loop
            if not posts:
                print_error(f"{username}: No more posts to interact with.")
                break

            for post in posts:
                try:
                    # Check if the total time limit has been reached
                    if (time.time() - start_time) >= total_time:
                        print(
                            f"{username} : Time limit of {total_time} seconds reached."
                        )
                        print(
                            f"{username} : Finished interacting with {interacted_posts} posts."
                        )
                        return

                    post_id = post["pk"]
                    post_id_str = post["id"]

                    # Simulate time spent on post
                    time_on_post = random.uniform(
                        5, 25
                    )  # Spend 5 to 25 seconds on each post
                    print(
                        f"{username} : Viewing post {post_id} for {time_on_post:.2f} seconds..."
                    )
                    api.media_seen([post_id_str])  # Mark the media as seen
                    time.sleep(time_on_post)

                    # Check if the caption contains any of the specified keywords
                    caption_text = post.get("caption", {}).get("text", "")
                    contains_keyword = False

                    if keywords:
                        # Check if any keywords are found in the caption
                        contains_keyword = any(
                            keyword.lower() in caption_text.lower()
                            for keyword in keywords
                        )

                        if contains_keyword:
                            print(f"{username} : Post {post_id} contains keywords.")

                    # Adjust the action and comment probabilities based on whether keywords were found
                    effective_action_probability = (
                        action_probability * keyword_action_boost
                        if contains_keyword
                        else action_probability
                    )
                    effective_comment_probability = effective_action_probability / 2

                    # Randomly decide whether to like the post
                    if random.random() < effective_action_probability:
                        api.media_like(post_id)
                        print(f"{username} -- Liked post {post_id}.")

                    # Randomly decide whether to comment on the post
                    if (
                        random.random() < effective_comment_probability
                        and comments_list
                    ):
                        comment = random.choice(comments_list)
                        api.media_comment(post_id, comment)
                        print(f"{username} -- Commented on post {post_id}: {comment}")

                    interacted_posts += 1

                except Exception as e:
                    # If feedback_required error occurs, shut down immediately
                    error_message = str(e)
                    if "feedback_required" in error_message:
                        print_error(
                            f"{username} : Critical error encountered: {error_message}"
                        )
                        print_error(
                            f"{username} : Shutting down function to avoid Instagram rate-limiting issues."
                        )
                        return

                    # Skip the problematic post but continue the loop for minor errors
                    print_error(
                        f"{username} : Skipping post {post_id} due to error: {error_message}"
                    )
                    continue

            # Fetch more posts if time is still remaining
            print(f"{username} : Fetching more posts...")

        print(
            f"{username} : Finished interacting with {interacted_posts} posts in {total_time} seconds."
        )

    except Exception as e:
        print_error(f"{username} : An error occurred while scrolling: {str(e)}")
