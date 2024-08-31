from modules.utils import print_error, print_success


from modules.utils import print_error, print_success


def initial_follow_accounts(api):
    """
    Follow multiple Instagram accounts using the provided API client.

    :param api: The authenticated instagrapi Client instance.
    """
    usernames_to_follow = [
        "creators",
        "brainrot.network",
    ]  # Hardcoded list of usernames to follow

    for username in usernames_to_follow:
        try:
            user_id = api.user_id_from_username(username)
            if api.user_follow(user_id):
                print(f"Successfully followed the account '{username}'.")
            else:
                print_error(f"Failed to follow the account '{username}'.")
        except Exception as e:
            print_error(f"Error occurred while trying to follow '{username}': {e}")

    print_success("Followed all the initial follow accounts")


def should_save_reel(post):
    """
    Check if the reel should be saved based on the number of views.

    :param post: The Instaloader Post object.
    :return: True if the reel should be saved, False otherwise.
    """
    MIN_VIEWS = 10000
    try:
        if post.video_view_count is not None and post.video_view_count >= MIN_VIEWS:
            return True
        else:
            print(
                f"Skipping Reel {post.shortcode} due to insufficient views: {post.video_view_count} views."
            )
            return False
    except AttributeError:
        print_error(f"Could not retrieve view count for Reel {post.shortcode}.")
        return False
