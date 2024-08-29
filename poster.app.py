from modules.poster import (
    post_reel_to_all_accounts,
    post_reel_single_account,
    posting_strategy_1,
)
from modules.utils import (
    print_header,
    print_error,
    get_user_input,
    wait_for_enter,
)
import sys


def main():
    actions = {
        1: post_reel_to_all_accounts,
        2: post_reel_single_account,
        3: posting_strategy_1,
        4: sys.exit,
    }

    while True:
        wait_for_enter()
        print_header("Post Reels")
        print("1. Post to all accounts")
        print("2. Post to single account")
        print("3. Post to all accounts, S1")
        print("4. Exit")

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
