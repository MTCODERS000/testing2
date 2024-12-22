import random
import string
import requests
import os
import time
from threading import Thread
from queue import Queue
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama for cross-platform support
init()

# Constants
THREAD_COUNT = 10
CODES_PER_THREAD = 5
DELAY = 1  # Delay per thread in seconds

# Shared counters
generated_count = 0
valid_count = 0
invalid_count = 0

# Queue for generated codes
code_queue = Queue()

# Lock to manage console output synchronization
from threading import Lock
lock = Lock()

def random_code():
    """Generates a random Discord Nitro code with 16 or 19 characters."""
    length = random.choice([16, 19])
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_code(code):
    """Checks if a Discord Nitro code is valid."""
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def worker_thread():
    """Thread function to generate and check codes."""
    global generated_count, valid_count, invalid_count

    valid_codes_file = "valid_codes.txt"

    while True:
        codes = [random_code() for _ in range(CODES_PER_THREAD)]
        for code in codes:
            # Check code validity
            is_valid = check_code(code)
            
            with lock:
                generated_count += 1
                if is_valid:
                    valid_count += 1
                    print(Fore.GREEN + Style.BRIGHT + f"🎉 VALID CODE FOUND: https://discord.gift/{code} 🎉" + Style.RESET_ALL)
                    # Save valid code to file
                    with open(valid_codes_file, "a") as file:
                        file.write(f"https://discord.gift/{code}\n")
                else:
                    invalid_count += 1

                # Update stats in console
                os.system("clear")
                banner = pyfiglet.figlet_format("Discord Nitro")
                print(Fore.MAGENTA + banner + Style.RESET_ALL)
                print(Fore.YELLOW + "✨ Auto-Creating and Checking Discord Nitro Gift Codes ✨" + Style.RESET_ALL)
                print(Fore.CYAN + f"Number of gift codes generated = {generated_count}" + Style.RESET_ALL)
                print(Fore.GREEN + f"Valid codes = {valid_count}" + Style.RESET_ALL)
                print(Fore.RED + f"Invalid codes = {invalid_count}" + Style.RESET_ALL)
                print(Fore.YELLOW + f"Latest code checked: https://discord.gift/{code}" + Style.RESET_ALL)
        
        time.sleep(DELAY)

def main():
    os.system('clear')  # Clear the console
    banner = pyfiglet.figlet_format("Discord Nitro")
    print(Fore.MAGENTA + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "✨ Auto-Creating and Checking Discord Nitro Gift Codes ✨" + Style.RESET_ALL)

    # Start worker threads
    threads = []
    for _ in range(THREAD_COUNT):
        thread = Thread(target=worker_thread)
        thread.daemon = True  # Daemon thread stops with the main program
        thread.start()
        threads.append(thread)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting... Bye! 👋" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
    
