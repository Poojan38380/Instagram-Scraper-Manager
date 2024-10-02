from modules.poster import (
    delete_reel_for_selected_account,
    delete_reels_below_threshold,
    post_reel_multiple_times_for_account,
    post_reel_multiple_accounts,
    post_reel_to_all_accounts,
    single_account_flush,
    post_reel_single_account,
    posting_strategy_1,
    all_accounts_flush,
)
from modules.utils import (
    print_header,
    print_error,
    get_user_input,
    
)
import sys


def main():
    actions = {
        1: post_reel_to_all_accounts,
        2: post_reel_single_account,
        3: posting_strategy_1,
        4: post_reel_multiple_accounts,
        5: single_account_flush,
        6: all_accounts_flush,
        7: delete_reel_for_selected_account,
        8: post_reel_multiple_times_for_account,
        9: delete_reels_below_threshold,
        10: sys.exit,
    }

    while True:
        print_header("Post Reels")
        print("1. Post to all accounts")
        print("2. Post to single account")
        print("3. Post to all accounts, S1")
        print("4. Post to multiple accounts")
        print("5. Single account flush")
        print("6. All Account Flush")
        print("7. Delete a reel")
        print("8. Post reels multiple times for an account")
        print("9. Delete low performing reels")
        print("10. Exit")

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
