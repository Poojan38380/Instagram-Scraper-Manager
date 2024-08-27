from colorama import init, Fore, Style
import sys
import random


# Initialize colorama
init(autoreset=True)


def print_header(message):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL}")


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


def get_random_member(array):
    if not array:
        return None  # Return None if the array is empty
    return random.choice(array)
