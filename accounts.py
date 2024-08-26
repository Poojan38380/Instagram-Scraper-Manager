from pymongo import MongoClient
from dotenv import load_dotenv
import os
from utils import (
    print_header,
    print_error,
    print_success,
    get_user_input,
)


# Load environment variables from .env file
load_dotenv()

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.instaposter
accounts_collection = db.accounts


def select_account_action(action_message):
    accounts = list(accounts_collection.find({}, {"username": 1}))

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

    if accounts_collection.find_one({"username": username}):
        print_error(
            f"Username '{username}' already exists. Please choose a different one."
        )
        return

    accounts_collection.insert_one({"username": username, "password": password})
    print_success(f"Account for '{username}' added successfully.")


def add_scraping_accounts():
    selected_username = select_account_action(
        "Select an account to add scraping accounts:"
    )
    if not selected_username:
        return

    existing_account = accounts_collection.find_one({"username": selected_username})
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

    updated_scraping_accounts = existing_scraping_accounts + new_scraping_accounts
    accounts_collection.update_one(
        {"username": selected_username},
        {"$set": {"scraping_accounts": updated_scraping_accounts}},
    )

    print_success(f"Scraping accounts added to '{selected_username}' successfully.")

    # Show the updated list of scraping accounts
    view_scraping_accounts_by_username(selected_username)


def view_scraping_accounts():
    selected_username = select_account_action(
        "Select an account to view its scraping accounts:"
    )
    if not selected_username:
        return

    view_scraping_accounts_by_username(selected_username)


def remove_scraping_account():
    selected_username = select_account_action(
        "Select an account to manage its scraping accounts:"
    )
    if not selected_username:
        return

    account_data = accounts_collection.find_one(
        {"username": selected_username}, {"scraping_accounts": 1}
    )
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


def view_scraping_accounts_by_username(selected_username):
    account_data = accounts_collection.find_one(
        {"username": selected_username}, {"scraping_accounts": 1}
    )
    scraping_accounts = account_data.get("scraping_accounts", [])

    if scraping_accounts:
        print_header(f"Scraping accounts for '{selected_username}':")
        for index, scrape_account in enumerate(scraping_accounts, start=1):
            print(f"{index}. {scrape_account}")
    else:
        print_error(f"No scraping accounts found for '{selected_username}'.")
