from modules.mongo import db
from modules.auth import login
from modules.utils import (
    print_header,
    print_error,
    print_success,
    get_user_input,
)
from modules.misc import initial_follow_accounts

accounts_collection = db.accounts
posted_reels_collection = db.posted_reels


def select_account_action(action_message):
    try:
        accounts = list(accounts_collection.find({}, {"username": 1}))
    except Exception as e:
        print_error(f"Failed to retrieve accounts: {e}")
        return None

    if not accounts:
        print_error("No accounts found in the database.")
        return None

    print_header(action_message)
    for index, account in enumerate(accounts, start=1):
        print(f"{index}. {account['username']}")

    try:
        choice = int(get_user_input("Enter the account number: "))
        if 1 <= choice <= len(accounts):
            return accounts[choice - 1]["username"]
        else:
            print_error("Invalid selection. Please choose a valid number.")
    except ValueError:
        print_error("Please enter a valid number.")
    return None


def add_new_account():
    print_header("Create a new account")
    username = get_user_input("Enter username: ")
    password = get_user_input("Enter password: ")

    if not username or not password:
        print_error("Username and password cannot be empty.")
        return

    try:
        if accounts_collection.find_one({"username": username}):
            print_error(
                f"Username '{username}' already exists. Please choose a different one."
            )
            return
    except Exception as e:
        print_error(f"Failed to check for existing username: {e}")
        return

    api = login(username, password)

    if api is None:
        print_error("Failed to login. Check your credentials and try again.")
        return

    try:
        accounts_collection.insert_one({"username": username, "password": password})
        print_success(f"Account for '{username}' added successfully.")
    except Exception as e:
        print_error(f"Failed to add account: {e}")

    # New function call to follow the "creators" account
    initial_follow_accounts(api)


def add_scraping_accounts():
    selected_username = select_account_action(
        "Select an account to add scraping accounts:"
    )
    if not selected_username:
        return

    existing_account = accounts_collection.find_one({"username": selected_username})

    if not existing_account:
        print_error(f"Account '{selected_username}' not found.")
        return

    existing_scraping_accounts = existing_account.get("scraping_accounts", [])

    scraping_accounts_input = get_user_input(
        "Enter usernames to scrape, separated by commas: "
    )
    if not scraping_accounts_input:
        print_error("No scraping accounts provided.")
        return

    new_scraping_accounts = [
        username
        for username in map(str.strip, scraping_accounts_input.split(","))
        if username and username not in existing_scraping_accounts
    ]

    if not new_scraping_accounts:
        print_error("No new scraping accounts to add.")
        return

    try:
        accounts_collection.update_one(
            {"username": selected_username},
            {
                "$set": {
                    "scraping_accounts": existing_scraping_accounts
                    + new_scraping_accounts
                }
            },
        )
        print_success(f"Scraping accounts added to '{selected_username}' successfully.")
        view_scraping_accounts_by_username(selected_username)
    except Exception as e:
        print_error(f"Failed to update scraping accounts: {e}")


def view_scraping_accounts():
    selected_username = select_account_action(
        "Select an account to view its scraping accounts:"
    )
    if selected_username:
        view_scraping_accounts_by_username(selected_username)


def remove_scraping_account():
    selected_username = select_account_action(
        "Select an account to manage its scraping accounts:"
    )
    if not selected_username:
        return

    account_data = accounts_collection.find_one({"username": selected_username})
    if not account_data:
        print_error(f"Account '{selected_username}' not found.")
        return

    scraping_accounts = account_data.get("scraping_accounts", [])

    if not scraping_accounts:
        print_error(f"No scraping accounts found for '{selected_username}'.")
        return

    print_header(f"Scraping accounts for '{selected_username}':")
    for index, scrape_account in enumerate(scraping_accounts, start=1):
        print(f"{index}. {scrape_account}")

    try:
        scrape_choice = int(
            get_user_input("Enter the number of the scraping account to remove: ")
        )
        if 1 <= scrape_choice <= len(scraping_accounts):
            scrape_to_remove = scraping_accounts[scrape_choice - 1]
            updated_scraping_accounts = [
                acc for acc in scraping_accounts if acc != scrape_to_remove
            ]

            accounts_collection.update_one(
                {"username": selected_username},
                {"$set": {"scraping_accounts": updated_scraping_accounts}},
            )

            print_success(
                f"Scraping account '{scrape_to_remove}' removed from '{selected_username}' successfully."
            )
            view_scraping_accounts_by_username(selected_username)
        else:
            print_error("Invalid selection. Please choose a valid number.")
    except ValueError:
        print_error("Please enter a valid number.")
    except Exception as e:
        print_error(f"Failed to update scraping accounts: {e}")


def remove_scraping_account_by_username(username, scraping_account_to_remove):
    try:
        # Retrieve the account data for the specified username
        account_data = accounts_collection.find_one({"username": username})

        if not account_data:
            print_error(f"Account '{username}' not found.")
            return False

        # Get the list of scraping accounts for the user
        scraping_accounts = account_data.get("scraping_accounts", [])

        if scraping_account_to_remove not in scraping_accounts:
            print_error(
                f"Scraping account '{scraping_account_to_remove}' not found for '{username}'."
            )
            return False

        # Update the scraping accounts list by removing the specified account
        updated_scraping_accounts = [
            account
            for account in scraping_accounts
            if account != scraping_account_to_remove
        ]

        # Update the user's scraping accounts in the database
        accounts_collection.update_one(
            {"username": username},
            {"$set": {"scraping_accounts": updated_scraping_accounts}},
        )

        print_success(
            f"Scraping account '{scraping_account_to_remove}' removed from '{username}' successfully."
        )
        return True
    except Exception as e:
        print_error(f"Failed to remove scraping account: {e}")
        return False


def view_scraping_accounts_by_username(selected_username):

    account_data = accounts_collection.find_one({"username": selected_username})

    if not account_data:
        print_error(f"Account '{selected_username}' not found.")
        return

    scraping_accounts = account_data.get("scraping_accounts", [])

    if scraping_accounts:
        print_header(f"Scraping accounts for '{selected_username}':")
        for index, scrape_account in enumerate(scraping_accounts, start=1):
            print(f"{index}. {scrape_account}")
    else:
        print_error(f"No scraping accounts found for '{selected_username}'.")


def get_scraping_accounts(selected_username):
    account_data = accounts_collection.find_one({"username": selected_username})

    if not account_data:
        print_error(f"Account '{selected_username}' not found.")
        return []

    return account_data.get("scraping_accounts", [])


def get_all_usernames():
    try:
        usernames = list(accounts_collection.find({}, {"_id": 0, "username": 1}))
    except Exception as e:
        print_error(f"Failed to retrieve usernames: {e}")
        return []

    if not usernames:
        print_error("No accounts found in the database.")
        return []

    return [user["username"] for user in usernames]


def get_password_by_username(username):
    try:
        account = accounts_collection.find_one({"username": username}, {"password": 1})
    except Exception as e:
        print_error(f"Failed to retrieve password: {e}")
        return None

    if account:
        return account.get("password")
    else:
        print_error(f"Username '{username}' not found.")
        return None


def get_all_usernames_and_passwords():
    try:
        users = list(
            accounts_collection.find({}, {"_id": 0, "username": 1, "password": 1})
        )
    except Exception as e:
        print_error(f"Failed to retrieve users: {e}")
        return []

    if not users:
        print_error("No accounts found in the database.")
        return []

    return [
        {"username": user["username"], "password": user["password"]} for user in users
    ]


def add_reel_to_user(username, reel_code):
    try:
        account = accounts_collection.find_one({"username": username})
    except Exception as e:
        print_error(f"Failed to retrieve account: {e}")
        return

    if not account:
        print_error(f"Username '{username}' not found.")
        return

    try:
        posted_reels_collection.insert_one(
            {"username": username, "reel_code": reel_code}
        )
        accounts_collection.update_one(
            {"username": username},
            {"$addToSet": {"reel_codes": reel_code}},  # $addToSet prevents duplicates
        )
        print_success(f"Reel '{reel_code}' added to '{username}' successfully.")
    except Exception as e:
        print_error(f"Failed to add reel: {e}")


def is_reel_posted_by_user(username, reel_code):
    try:
        account = accounts_collection.find_one(
            {"username": username, "reel_codes": reel_code}
        )
        return account is not None
    except Exception as e:
        print_error(f"Failed to check reel posting: {e}")
        return False
