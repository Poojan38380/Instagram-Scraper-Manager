import random
import time
import json
from modules.utils import print_error

comments = [
    "This is so relatable! Anyone else feel the same? 😄",
    "I love this! What do you guys think? 🤔",
    "Wow, this just made my day! Who else agrees? 💯",
    "This is so cool! Anyone else tried this? 🔥",
    "Such good vibes! Who's feeling the same energy? ✨",
    "Haha, this is gold! Anyone else laughing at this? 😂",
    "I can't stop watching this! Anyone else obsessed? 😍",
    "This is super inspiring! Anyone else motivated by this? 💪",
    "Absolutely love this! What's everyone’s take on it? ❤️",
    "This deserves more attention! Who agrees? 🚀",
    "I was just thinking about this! Anyone else? 😲",
    "Wow, I'm learning so much from this! Who’s with me? 📚",
    "This is the kind of content we need more of! Who agrees? 🙌",
    "I'm curious, has anyone tried this? Thoughts? 🤔",
    "This is exactly what I needed today! Who else? 😎",
    "I can't be the only one obsessed with this! Who's with me? 👀",
    "Why is this so accurate?! 😂 Can anyone relate?",
    "This really hit home! Anyone else feel this way? 😢",
    "I could watch this all day! Who's with me? 😆",
    "Totally agree with this! Anyone else think the same? 👍",
]


def human_like_scrolling(
    api,
    username="",
    total_time=60,
    action_probability=0.4,
    keyword_action_boost=2,  # Additional boost for actions when keywords are found
    comments_list=comments,
    keywords=None,
    idle_chance=0.1,  # Chance to "do nothing" for a period of time
    idle_duration=(5, 20),  # Random idle time to simulate distraction
    typo_chance=0.05,  # Chance of a typo in comments
    max_typo_count=2,  # Max number of typos in a comment
):
    """
    Scrolls through the Instagram newsfeed or reel feed and interacts with posts in a human-like manner for a specified duration.
    Interacts with posts based on specific keywords in the caption if provided, with increased probability of liking/commenting.

    Args:
        api (Client): The instagrapi API client object.
        total_time (int): Total time to spend scrolling in seconds. Default is 60 seconds.
        action_probability (float): Base probability (0 to 1) of liking a post or viewing a reel. Default is 0.4.
        keyword_action_boost (float): Additional boost to action probability when keywords are found in the caption. Default is 2.
        comments_list (list): List of comments to randomly choose from when commenting. Default is None.
        keywords (list): List of keywords to check in the caption text. Default is None.
        idle_chance (float): Probability of taking an idle break. Default is 0.1 (10%).
        idle_duration (tuple): Range of seconds to stay idle during idle periods. Default is (5, 20).
        typo_chance (float): Probability of introducing a typo in a comment. Default is 0.05.
        max_typo_count (int): Maximum number of typos per comment. Default is 2.
    """

    start_time = time.time()  # Record the starting time
    interacted_posts = 0

    # If no keywords are provided, use an empty list
    if keywords is None:
        keywords = []

    def add_typos(text):
        """Simulates human typing errors."""
        if random.random() < typo_chance:
            typo_count = random.randint(1, max_typo_count)
            text_chars = list(text)
            for _ in range(typo_count):
                idx = random.randint(0, len(text_chars) - 1)
                text_chars[idx] = random.choice("abcdefghijklmnopqrstuvwxyz")
            return "".join(text_chars)
        return text

    try:
        while (time.time() - start_time) < total_time:
            # Simulate idle behavior
            if random.random() < idle_chance:
                idle_time = random.uniform(*idle_duration)
                print(f"{username} : Taking a break for {idle_time:.2f} seconds...")
                time.sleep(idle_time)

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
                        7, 35
                    )  # More randomness (7 to 35 seconds)
                    print(
                        f"{username} : Viewing post {post_id} for {time_on_post:.2f} seconds..."
                    )
                    api.media_seen([post_id_str])  # Mark the media as seen
                    time.sleep(time_on_post)

                    # Check if the caption contains any of the specified keywords
                    caption = post.get("caption")
                    caption_text = caption.get("text", "") if caption else ""
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
                        comment_with_typos = add_typos(
                            comment
                        )  # Add typos to the comment
                        api.media_comment(post_id, comment_with_typos)
                        print(
                            f"{username} -- Commented on post {post_id}: {comment_with_typos}"
                        )

                    interacted_posts += 1

                except Exception as e:
                    # Handle feedback_required error
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
