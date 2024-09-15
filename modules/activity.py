import random
import time
import json

comments = ["Nice post!", "Awesome!", "Great content!", "Love this!", "❤️❤️"]


def human_like_scrolling(
    api,
    username="",
    total_time=1800,
    action_probability=0.5,
    comment_probability=0.2,
    comments_list=comments,
):
    """
    Scrolls through the Instagram newsfeed or reel feed and interacts with posts in a human-like manner for a specified duration.

    Args:
        api (Client): The instagrapi API client object.
        total_time (int): Total time to spend scrolling in seconds. Default is 60 seconds.
        action_probability (float): Probability (0 to 1) of liking a post or viewing a reel. Default is 0.5.
        comment_probability (float): Probability (0 to 1) of commenting on a post. Default is 0.3.
        comments_list (list): List of comments to randomly choose from when commenting. Default is None.
    """

    start_time = time.time()  # Record the starting time
    interacted_posts = 0

    try:
        while (time.time() - start_time) < total_time:
            # Fetch the newsfeed/reel feed posts
            feed = api.get_timeline_feed()  # For newsfeed
            # feed = api.reels_tray()  # For reel feed

            if not feed or "feed_items" not in feed:
                print(f"{username} : No posts found.")
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
                print(f"{username}: No more posts to interact with.")
                break

            for post in posts:
                # Check if the total time limit has been reached
                if (time.time() - start_time) >= total_time:
                    print(f"{username} : Time limit of {total_time} seconds reached.")
                    print(
                        f"{username} : Finished interacting with {interacted_posts} posts."
                    )
                    return

                post_id = post["pk"]

                # Simulate time spent on post
                time_on_post = random.uniform(
                    5, 25
                )  # Spend 5 to 25 seconds on each post
                print(
                    f"{username} : Viewing post {post_id} for {time_on_post:.2f} seconds..."
                )
                time.sleep(time_on_post)

                # Randomly decide whether to like the post
                if random.random() < action_probability:
                    api.media_like(post_id)
                    print(f"{username} -- Liked post {post_id}.")

                # Randomly decide whether to comment on the post
                if random.random() < comment_probability and comments_list:

                    api.media_like(post_id)
                    print(f"{username} -- Liked post {post_id}.")

                    comment = random.choice(comments_list)
                    api.media_comment(post_id, comment)
                    print(f" {username} -- Commented on post {post_id}: {comment}")

                interacted_posts += 1

            # Fetch more posts if time is still remaining
            print("Fetching more posts...")

        print(
            f"{username} : Finished interacting with {interacted_posts} posts in {total_time} seconds."
        )

    except Exception as e:
        print(f"{username} : An error occurred while scrolling: {str(e)}")
