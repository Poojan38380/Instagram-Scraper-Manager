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
    keyword_action_boost=2,
    comments_list=comments,
    keywords=None,
):
    """
    Scrolls through the Instagram newsfeed or reel feed and interacts with posts in a human-like manner for a specified duration.
    """

    start_time = time.time()
    interacted_posts = 0
    keywords = keywords or []

    try:
        while time.time() - start_time < total_time:
            feed = api.get_timeline_feed()
            if not feed or "feed_items" not in feed:
                print_error(f"{username} : No posts found.")
                return

            posts = [
                item["media_or_ad"]
                for item in feed["feed_items"]
                if "media_or_ad" in item
            ]
            print(f"{username} : Retrieved {len(posts)} posts.")

            if not posts:
                print_error(f"{username} : No more posts to interact with.")
                break

            for post in posts:
                if time.time() - start_time >= total_time:
                    print(f"{username} : Time limit of {total_time} seconds reached.")
                    print(
                        f"{username} : Finished interacting with {interacted_posts} posts."
                    )
                    return

                post_id = post["pk"]
                post_id_str = post["id"]
                caption_text = post.get("caption", {}).get("text", "")

                # Simulate time spent on post
                time_on_post = random.uniform(5, 25)
                print(
                    f"{username} : Viewing post {post_id} for {time_on_post:.2f} seconds..."
                )
                api.media_seen([post_id_str])
                time.sleep(time_on_post)

                contains_keyword = any(
                    keyword.lower() in caption_text.lower() for keyword in keywords
                )

                if contains_keyword:
                    print(f"{username} : Post {post_id} contains keywords.")

                # Adjust action and comment probability
                effective_action_probability = action_probability * (
                    keyword_action_boost if contains_keyword else 1
                )

                if random.random() < effective_action_probability:
                    api.media_like(post_id)
                    print(f"{username} -- Liked post {post_id}.")

                if random.random() < effective_action_probability / 2 and comments_list:
                    comment = random.choice(comments_list)
                    api.media_comment(post_id, comment)
                    print(f"{username} -- Commented on post {post_id}: {comment}")

                interacted_posts += 1

            print(f"{username} : Fetching more posts...")

        print(
            f"{username} : Finished interacting with {interacted_posts} posts in {total_time} seconds."
        )

    except Exception as e:
        error_message = str(e)
        if "feedback_required" in error_message:
            print_error(f"{username} : Critical error encountered: {error_message}")
            print_error(
                f"{username} : Shutting down function to avoid Instagram rate-limiting issues."
            )
        else:
            print_error(
                f"{username} : An error occurred while scrolling: {error_message}"
            )
