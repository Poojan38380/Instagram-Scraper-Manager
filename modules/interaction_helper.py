from modules.mongo import db
import random


from modules.utils import print_error, print_success


comments_list = [
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


accounts_collection = db.accounts
posted_reels_collection = db.posted_reels


def save_last_interacted_reel(username, reel_pk):
    """
    Save the last interacted reel_pk for the specified username.

    Args:
        username (str): The username of the account.
        reel_pk (int): The primary key (identifier) of the interacted reel.
    """
    try:
        # Check if the user exists in the database
        account = accounts_collection.find_one({"username": username})
        if not account:
            print_error(f"Account '{username}' not found.")
            return

        # Update the last interacted reel for the user
        accounts_collection.update_one(
            {"username": username}, {"$set": {"last_interacted_reel": reel_pk}}
        )
        print(f"Last interacted reel '{reel_pk}' saved for user '{username}'.")
    except Exception as e:
        print_error(f"Failed to save last interacted reel: {e}")


def get_last_interacted_reel(username):
    """
    Retrieve the last interacted reel_pk for the specified username.

    Args:
        username (str): The username of the account.

    Returns:
        int: The primary key (identifier) of the last interacted reel, or None if not found.
    """
    try:
        # Fetch the account data from the database
        account = accounts_collection.find_one(
            {"username": username}, {"last_interacted_reel": 1}
        )

        if not account:
            print_error(f"Account '{username}' not found.")
            return None

        # Get the last interacted reel from the account data
        reel_pk = account.get("last_interacted_reel")

        if reel_pk is not None:
            print_success(f"Last interacted reel for '{username}' is '{reel_pk}'.")
            return reel_pk
        else:
            print_error(f"No last interacted reel found for '{username}'.")
            return None
    except Exception as e:
        print_error(f"Failed to retrieve last interacted reel: {e}")
        return None


def get_comment_for_reel(
    typo_chance=0.05,  # Chance of a typo in comments
    max_typo_count=2,  # Max number of typos in a comment
):
    comment = random.choice(comments_list)

    """Simulates human typing errors."""
    if random.random() < typo_chance:
        typo_count = random.randint(1, max_typo_count)
        text_chars = list(comment)
        for _ in range(typo_count):
            idx = random.randint(0, len(text_chars) - 1)
            text_chars[idx] = random.choice("abcdefghijklmnopqrstuvwxyz")
        return "".join(text_chars)
    return comment
