from instagrapi import Client

import os
import pickle
from modules.utils import print_header, print_error, print_success


def ensure_directory_exists(filepath: str) -> None:
    """
    Ensure that the directory for the given filepath exists.
    If it does not exist, create it.

    Args:
        filepath (str): The path to the file.
    """
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print_success(f"Directory '{directory}' created.")


def save_api_client(api: Client, username: str) -> None:
    """
    Save the authenticated API client to local storage.

    Args:
        api (Client): The authenticated instagrapi Client instance.
        username (str): The Instagram username.
    """
    api_storage_file = f"loginInfo/{username}/api_client.pkl"
    ensure_directory_exists(api_storage_file)
    try:
        with open(api_storage_file, "wb") as file:
            pickle.dump(api, file)
        print_success(f"API client for {username} saved to local storage.")
    except Exception as e:
        print_error(f"Failed to save API client for {username}: {str(e)}")


def load_api_client(username: str) -> Client:
    """
    Load the API client from local storage if it exists.

    Args:
        username (str): The Instagram username.

    Returns:
        Client: The instagrapi Client instance, or None if it doesn't exist.
    """
    api_storage_file = f"loginInfo/{username}/api_client.pkl"
    if os.path.exists(api_storage_file):
        try:
            with open(api_storage_file, "rb") as file:
                print_success(f"API client for {username} loaded from local storage.")
                return pickle.load(file)
        except Exception as e:
            print_error(f"Failed to load API client for {username}: {str(e)}")
    return None  # type: ignore


def login(username: str, password: str) -> Client:
    """
    Login to Instagram using instagrapi Client.

    Args:
        username (str): Instagram username.
        password (str): Instagram password.

    Returns:
        Client: An authenticated instagrapi Client instance.
    """
    try:
        # Try to load API client from local storage
        api = load_api_client(username)
        if api:
            return api

        print_header("Initializing login...")
        api = Client()
        api.delay_range = [1, 3]

        session_file = f"loginInfo/{username}/session.json"
        ensure_directory_exists(session_file)

        if os.path.exists(session_file):
            print_header("Logging in with previous session...")
            api.load_settings(session_file)  # type: ignore
            api.login(username, password)
        else:
            print_header("Logging in with username and password...")
            api.login(username, password)
            api.dump_settings(session_file)  # type: ignore

        # Verify login by fetching timeline feed
        api.get_timeline_feed()
        print_success("Logged in successfully.")

        # Save the API client to local storage for future use
        save_api_client(api, username)

        return api

    except Exception as e:
        if "login_required" in str(e):
            print_error("Login failed. Please check your username and password.")
        elif "challenge_required" in str(e):
            print_error(
                "Instagram has flagged this login attempt. Please check your account for security challenges."
            )
        else:
            print_error(f"An unexpected error occurred during login: {str(e)}")
        raise e  # Re-raise the exception for further handling if needed
