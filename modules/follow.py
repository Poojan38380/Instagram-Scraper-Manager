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
