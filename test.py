import sys
from accounts import (
    add_new_account,
    add_scraping_accounts,
    view_scraping_accounts,
    remove_scraping_account,
)
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


def print_header(message):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL}\n")


def print_error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def get_user_input(prompt):
    return input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip()


def wait_for_enter():
    user_input = get_user_input("Press Enter to proceed")
    if user_input != "":
        print_error("Exiting as user pressed a key other than Enter.")
        sys.exit(0)


def main():
    actions = {
        1: add_new_account,
        2: add_scraping_accounts,
        3: view_scraping_accounts,
        4: remove_scraping_account,
        5: sys.exit,
    }

    while True:
        wait_for_enter()
        print_header("Account Management System")
        print("1. Add New Account")
        print("2. Add Scraping Accounts")
        print("3. View Scraping Accounts")
        print("4. Remove Scraping Account")
        print("5. Exit")

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
