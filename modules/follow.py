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


def follow_accounts(api, accounts_to_follow):
    """
    Follow multiple Instagram accounts for a given user using the provided API client.

    :param username: The username of the person initiating the follows.
    :param accounts_to_follow: A list of Instagram account usernames to follow.
    """
    try:

        print(f"Initiating follow actions for user '{username}'.")

        for account in accounts_to_follow:
            try:
                account_id = api.user_id_from_username(account)
                if api.user_follow(account_id):
                    print(
                        f"'{username}' successfully followed the account '{account}'."
                    )
                else:
                    print_error(
                        f"Failed to follow the account '{account}' for user '{username}'."
                    )
            except Exception as e:
                print_error(
                    f"Error occurred while '{username}' tried to follow '{account}': {e}"
                )

        print_success(f"'{username}' followed all the provided accounts.")

    except Exception as e:
        print_error(f"Error occurred while fetching user ID for '{username}': {e}")
