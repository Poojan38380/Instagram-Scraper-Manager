import sys
from modules.accounts import (
    add_new_account,
    add_scraping_accounts,
    add_tagline_to_account,
    view_scraping_accounts,
    remove_scraping_account,
    add_caption_to_account,
)

from modules.utils import (
    print_header,
    print_error,
    get_user_input,
    wait_for_enter,
)


def main():
    actions = {
        1: add_new_account,
        2: add_scraping_accounts,
        3: view_scraping_accounts,
        4: remove_scraping_account,
        5: add_caption_to_account,
        6: add_tagline_to_account,
        7: sys.exit,
    }

    while True:
        wait_for_enter()
        print_header("Account Management System")
        print("1. Add New Account")
        print("2. Add Scraping Accounts")
        print("3. View Scraping Accounts")
        print("4. Remove Scraping Account")
        print("5. Add Caption/Hastags to Account")
        print("6. Add Tagline to Account")
        print("7. Exit")

        try:
            action = int(get_user_input("Choose an action: "))
            if action in actions:
                actions[action]()
            else:
                print_error("Invalid selection. Please choose a valid number.")
        except ValueError:
            print_error("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nProcess interrupted by user.\n")
            sys.exit(0)
        except Exception as e:
            print_error(f"Main process error: {str(e)}")


if __name__ == "__main__":
    main()
