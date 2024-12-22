import random
import string
import requests
import os
import time
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama for cross-platform support
init()

def random_code():
    length = random.choice([16, 19])  # Randomly select 16 or 19
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def check_code(code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def main():
    os.system('clear')  # Clear console
    banner = pyfiglet.figlet_format("Discord Nitro")
    print(Fore.MAGENTA + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "✨ Auto-Creating and Checking Discord Nitro Gift Codes ✨" + Style.RESET_ALL)

    generated_count = 0
    valid_count = 0
    invalid_count = 0

    valid_codes_file = "valid_codes.txt"

    if os.path.exists(valid_codes_file):
        os.remove(valid_codes_file)  # Remove file if it exists

    while True:
        code = random_code()
        generated_count += 1

        # Print stats and code
        print(Fore.CYAN + f"\rNumber of gift codes generated = {generated_count}", end="")
        print(Fore.GREEN + f"\rValid codes = {valid_count}", end="")
        print(Fore.RED + f"\rInvalid codes = {invalid_count}", end="")
        print(Fore.YELLOW + f"\rhttps://discord.gift/{code}", end="", flush=True)

        # Check if the code is valid
        if check_code(code):
            valid_count += 1
            print("\n" + Fore.GREEN + Style.BRIGHT + f"🎉 VALID CODE FOUND: https://discord.gift/{code} 🎉" + Style.RESET_ALL)
            with open(valid_codes_file, "a") as file:
                file.write(f"https://discord.gift/{code}\n")
        else:
            invalid_count += 1

        # Small delay to simulate generation and checking
        time.sleep(0.1)

if __name__ == "__main__":
    main()
      
