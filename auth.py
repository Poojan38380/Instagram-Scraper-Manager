from instagrapi import Client
import os
import pickle

SESSION_FILE = "loginInfo/session.json"
API_STORAGE_FILE = "loginInfo/api_client.pkl"


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
        print(f"Directory '{directory}' created.")


def save_api_client(api: Client) -> None:
    """
    Save the authenticated API client to local storage.

    Args:
        api (Client): The authenticated instagrapi Client instance.
    """
    ensure_directory_exists(API_STORAGE_FILE)
    with open(API_STORAGE_FILE, "wb") as file:
        pickle.dump(api, file)
    print("API client saved to local storage.")


def load_api_client() -> Client:
    """
    Load the API client from local storage if it exists.

    Returns:
        Client: The instagrapi Client instance, or None if it doesn't exist.
    """
    if os.path.exists(API_STORAGE_FILE):
        with open(API_STORAGE_FILE, "rb") as file:
            print("API client loaded from local storage.")
            return pickle.load(file)
    return None


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
        api = load_api_client()
        if api:
            return api

        print("Initializing login...")
        api = Client()
        api.delay_range = [1, 3]

        ensure_directory_exists(SESSION_FILE)

        if os.path.exists(SESSION_FILE):
            print("Logging in with previous session...")
            api.load_settings(SESSION_FILE)
            api.login(username, password)
        else:
            print("Logging in with username and password...")
            api.login(username, password)
            api.dump_settings(SESSION_FILE)

        # Verify login by fetching timeline feed
        api.get_timeline_feed()
        print("Logged in successfully.")

        # Save the API client to local storage for future use
        save_api_client(api)

        return api

    except Exception as e:
        print(f"An error occurred during login, check the login function: {str(e)}")
        if "login_required" in str(e):
            print("Login failed. Please check your username and password.")
        elif "challenge_required" in str(e):
            print(
                "Instagram has flagged this login attempt. Please check your account for security challenges."
            )
        else:
            print(
                "An unexpected error occurred. Please check the details and try again."
            )
        raise e  # Re-raise the exception for further handling if needed
