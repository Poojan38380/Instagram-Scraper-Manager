import sys
from modules.accounts import (
    add_new_account,
    add_scraping_accounts,
    add_tagline_to_account,
    view_scraping_accounts,
    remove_scraping_account,
    add_caption_to_account,
    add_keywords_to_account,
)

from modules.interact import explore_reels_all_accounts, explore_reels_for_single
from modules.interaction_feed import explore_feed_all_accounts
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
        3: add_tagline_to_account,
        4: remove_scraping_account,
        5: add_caption_to_account,
        6: view_scraping_accounts,
        7: add_keywords_to_account,
        8: explore_reels_for_single,
        9: explore_reels_all_accounts,
        10: explore_feed_all_accounts,
        11: sys.exit,
    }

    while True:
        wait_for_enter()
        print_header("Account Management System")
        print("1. Add New Account")
        print("2. Add Scraping Accounts")
        print("3. Add Tagline to Account")
        print("4. Remove Scraping Account")
        print("5. Add Caption/Hastags to Account")
        print("6. View Scraping Accounts")
        print("7. Add keywords to Account")
        print("8. Explore reels for single account")
        print("9. Explore reels for ALL account")
        print("10. Explore feed for all accounts")
        print("11. Exit")

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
