import random
import string
import requests
import os
import time
import platform
from threading import Thread
from queue import Queue
from colorama import Fore, Style, init
import pyfiglet
import psutil  # For CPU analysis

# Initialize colorama for cross-platform support
init()

# Shared counters
generated_count = 0
valid_count = 0
invalid_count = 0

# Lock for synchronized console output
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

def analyze_device():
    """Analyzes the device and recommends a number of threads."""
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq().max if psutil.cpu_freq() else 1000  # MHz
    ram = psutil.virtual_memory().total / (1024 ** 3)  # GB

    recommendation = min(cpu_count * 2, 50)  # Balance CPU threads with limits
    return cpu_count, cpu_freq, ram, recommendation

def worker_thread(codes_per_second):
    """Thread function to generate and check codes."""
    global generated_count, valid_count, invalid_count

    valid_codes_file = "valid_codes.txt"

    while True:
        codes = [random_code() for _ in range(codes_per_second)]
        for code in codes:
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
                print(Fore.CYAN + f"\rGenerated: {generated_count} | " +
                      Fore.GREEN + f"Valid: {valid_count} | " +
                      Fore.RED + f"Invalid: {invalid_count} | " +
                      Fore.YELLOW + f"Latest: https://discord.gift/{code}  ", end="")

def main():
    os.system('clear')  # Clear the console
    banner = pyfiglet.figlet_format("Discord Nitro")
    print(Fore.MAGENTA + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "✨ Auto-Creating and Checking Discord Nitro Gift Codes ✨" + Style.RESET_ALL)

    # Analyze the device and recommend threads
    cpu_count, cpu_freq, ram, recommendation = analyze_device()
    print(Fore.CYAN + f"Your Device Info:" + Style.RESET_ALL)
    print(Fore.CYAN + f" - CPU Cores: {cpu_count}")
    print(Fore.CYAN + f" - CPU Frequency: {cpu_freq:.2f} MHz")
    print(Fore.CYAN + f" - RAM: {ram:.2f} GB")
    print(Fore.GREEN + f"\nRecommended Threads: {recommendation}" + Style.RESET_ALL)

    # Ask the user how many threads they want
    try:
        threads = int(input(Fore.YELLOW + "\nHow many threads would you like to use? (e.g., 1-50): " + Style.RESET_ALL))
        if threads < 1 or threads > 50:
            print(Fore.RED + "Please choose between 1 and 50 threads. Using recommended threads instead." + Style.RESET_ALL)
            threads = recommendation
    except ValueError:
        print(Fore.RED + "Invalid input. Using recommended threads." + Style.RESET_ALL)
        threads = recommendation

    # Ask the user how many codes per second per thread
    try:
        codes_per_second = int(input(Fore.YELLOW + "How many codes should each thread generate per second? (e.g., 1-10): " + Style.RESET_ALL))
        if codes_per_second < 1 or codes_per_second > 10:
            print(Fore.RED + "Please choose between 1 and 10. Defaulting to 5." + Style.RESET_ALL)
            codes_per_second = 5
    except ValueError:
        print(Fore.RED + "Invalid input. Defaulting to 5." + Style.RESET_ALL)
        codes_per_second = 5

    # Start worker threads
    threads_list = []
    for _ in range(threads):
        thread = Thread(target=worker_thread, args=(codes_per_second,))
        thread.daemon = True  # Daemon threads stop with the main program
        thread.start()
        threads_list.append(thread)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting... Bye! 👋" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
    
