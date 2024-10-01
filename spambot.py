import os
import time
import requests
import psutil
import random
import json
from colorama import init, Fore, Back, Style
import pyfiglet

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize colorama
init(autoreset=True)

logo = pyfiglet.figlet_format("CC spambot")
print(logo)
print(f'{Fore.BLACK + Back.MAGENTA} > scripted by @garurprani {Style.RESET_ALL}')
print(Fore.MAGENTA + "> Do Message spam/promotion on ChitChat.gg")
print(f'{Fore.MAGENTA}> GITHUB: https://github.com/garurprani/ChitChat-spambot {Style.RESET_ALL}')

# Function to handle user input for Chrome user data directory path
def get_chrome_user_data_path():
    path = input("Enter Chrome user data directory path (e.g., C:\\Users\\garurprani\\AppData\\Local\\Google\\Chrome\\User Data): ").strip()
    while not os.path.isdir(path):
        print(Fore.RED + "Invalid directory path. Please enter a valid path.")
        path = input("Enter Chrome user data directory path: ").strip()
    return path

# Function to display main menu and handle user choices
def main_menu():
    while True:
        print()
        print_section(' Main Menu ', {
            'Add more Auth-Tokens: add': '',
            'Show Auth-Tokens: show': '',
            'Update profile path: path': '',
            'Run the Script: run': '',
            'Exit script: exit': ''
        })

        choice = input("Enter your choice: ").strip()

        if choice == 'add':
            add_auth_token()
        elif choice == 'show':
            show_auth_tokens()
        elif choice == 'path':
            update_profile_path()
        elif choice == 'run':
            run_script()
        elif choice == 'exit':
            print("Exiting the script.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a valid option.")

# Function to add auth token with profile name
def add_auth_token():
    profile_name = input("Enter profile name: ").strip()
    auth_token = input("Enter auth token: ").strip()

    # Validate auth token format
    if not is_valid_auth_token(auth_token):
        print(Fore.RED + "Invalid auth token format. Auth token must be 183 characters long and contain '.' after 36th character.")
        return

    # Save auth token to auth_profile.txt
    with open('auth_profile.txt', 'a') as f:
        f.write(f'{profile_name}: "{auth_token}"\n')

    print(Fore.GREEN + f"Auth token added successfully for profile '{profile_name}'.")

# Function to check if auth token format is valid
def is_valid_auth_token(auth_token):
    if len(auth_token) != 183:
        return False
    if auth_token[36] != '.':
        return False
    return True

# Function to show auth tokens from auth_profile.txt
# Function to show auth tokens from auth_profile.txt
def show_auth_tokens():
    print("\nAuth Tokens:")
    with open('auth_profile.txt', 'r') as f:
        for line in f:
            profile_name, auth_token = line.strip().split(': ')
            # Truncate auth_token to show only the last 9 characters
            masked_token = auth_token[-9:]
            print(Fore.CYAN + f"{profile_name}: {'*' * (len(auth_token) - 9)}{masked_token}")


# Function to update Chrome user data path
def update_profile_path():
    current_path = get_saved_chrome_user_data_path()
    print(Fore.YELLOW + f"Current Chrome user data path: {current_path}")
    new_path = input("Enter new Chrome user data path: ").strip()

    while not os.path.isdir(new_path):
        print(Fore.RED + "Invalid directory path. Please enter a valid path.")
        new_path = input("Enter new Chrome user data path: ").strip()

    # Save new path for future use
    save_chrome_user_data_path(new_path)
    print(Fore.GREEN + "Chrome user data path updated successfully.")

# Function to save Chrome user data path
def save_chrome_user_data_path(path):
    with open('chrome_user_data_path.txt', 'w') as f:
        f.write(path)

# Function to retrieve saved Chrome user data path
def get_saved_chrome_user_data_path():
    if os.path.isfile('chrome_user_data_path.txt'):
        with open('chrome_user_data_path.txt', 'r') as f:
            return f.read().strip()
    else:
        return None

# Function to start Selenium and run the script
def run_script():
    auth_profiles = load_auth_profiles()

    if not auth_profiles:
        print(Fore.RED + "No auth profiles found. Please add auth tokens first.")
        return

    num_iterations = int(input("Enter how many times to alternate between match request and sending message: "))
    message = input("Enter the message to send: ")

    for profile_name, auth_token in auth_profiles:
        start_selenium(profile_name, auth_token, num_iterations, message)

# Function to load auth profiles from auth_profile.txt
def load_auth_profiles():
    auth_profiles = []
    with open('auth_profile.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                profile_name = parts[0].strip()
                auth_token = parts[1].strip().strip('"')
                auth_profiles.append((profile_name, auth_token))
    return auth_profiles

# Function to kill existing Chrome processes
def kill_existing_chrome_processes():
    for proc in psutil.process_iter():
        try:
            if proc.name() == 'chrome.exe':
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Function to send match request
def send_match_request(token):
    url = "https://api.chitchat.gg/match"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": f"token={token}"
    }
    data = {}  # Add any required data for the match request

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(Fore.GREEN + "Match request successful.")
    else:
        print(Fore.RED + f"Failed to send match request. Status code: {response.status_code}")
        return None

    return response.json()  # Return JSON response if needed

# Function to send message
def send_message(driver, message):
    try:
        message_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-label='Send a message']"))
        )
        message_box.clear()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        print(Fore.GREEN + f"Message '{message}' sent successfully.")
    except Exception as e:
        print(Fore.RED + f"Failed to send message: {str(e)}")

# Function to start Selenium with specified profile and auth token
def start_selenium(profile_name, auth_token, num_iterations, message):
    kill_existing_chrome_processes()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    webdriver_path = os.path.join(script_dir, 'chromedriver.exe')

    if not os.path.isfile(webdriver_path):
        raise FileNotFoundError(f"Chromedriver not found at path: {webdriver_path}")

    service = Service(webdriver_path)
    user_data_dir = get_saved_chrome_user_data_path()

    if not user_data_dir:
        print(Fore.RED + "Chrome user data path not found. Please update the path.")
        return

    options = Options()
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"profile-directory={profile_name}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://app.chitchat.gg/start/new')
        time.sleep(5)

        for i in range(num_iterations):
            match_response = send_match_request(auth_token)
            if not match_response:
                print(Fore.RED + "Exiting due to match request failure.")
                break
            time.sleep(5)

            send_message(driver, message)
            time.sleep(5)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def main():
    chrome_user_data_path = get_saved_chrome_user_data_path()

    if not chrome_user_data_path:
        chrome_user_data_path = get_chrome_user_data_path()
        save_chrome_user_data_path(chrome_user_data_path)

    main_menu()

# Function to display colored section with options
def print_section(title, options):
    print(Fore.BLACK + Back.YELLOW + title)
    for key, value in options.items():
        option_name, command = key.split(': ')
        print(f'{Fore.GREEN + option_name}: {Fore.WHITE + command}')
    print(Style.RESET_ALL)

# Function to start the script
def start_script():
    chrome_user_data_path = get_saved_chrome_user_data_path()

    if not chrome_user_data_path:
        chrome_user_data_path = get_chrome_user_data_path()
        save_chrome_user_data_path(chrome_user_data_path)

    main_menu()

# Function to display colored section with options
def print_section(title, options):
    print(Fore.BLACK + Back.YELLOW + title)
    for key, value in options.items():
        option_name, command = key.split(': ')
        print(f'{Fore.GREEN + option_name}: {Fore.WHITE + command}')
    print(Style.RESET_ALL)

# Function to handle user input for Chrome user data directory path
def get_chrome_user_data_path():
    path = input("Enter Chrome user data directory path (e.g., C:\\Users\\dazzf\\AppData\\Local\\Google\\Chrome\\User Data): ").strip()
    while not os.path.isdir(path):
        print(Fore.RED + "Invalid directory path. Please enter a valid path.")
        path = input("Enter Chrome user data directory path: ").strip()
    return path

# Function to update Chrome user data path
def update_profile_path():
    current_path = get_saved_chrome_user_data_path()
    print(Fore.YELLOW + f"Current Chrome user data path: {current_path}")
    new_path = input("Enter new Chrome user data path: ").strip()

    while not os.path.isdir(new_path):
        print(Fore.RED + "Invalid directory path. Please enter a valid path.")
        new_path = input("Enter new Chrome user data path: ").strip()

    # Save new path for future use
    save_chrome_user_data_path(new_path)
    print(Fore.GREEN + "Chrome user data path updated successfully.")

# Function to save Chrome user data path
def save_chrome_user_data_path(path):
    with open('chrome_user_data_path.txt', 'w') as f:
        f.write(path)

# Function to retrieve saved Chrome user data path
def get_saved_chrome_user_data_path():
    if os.path.isfile('chrome_user_data_path.txt'):
        with open('chrome_user_data_path.txt', 'r') as f:
            return f.read().strip()
    else:
        return None

# Function to add auth token with profile name
def add_auth_token():
    chrome_user_data_path = get_saved_chrome_user_data_path()
    if not chrome_user_data_path:
        print(Fore.RED + "Chrome user data path not found. Please update the path.")
        return

    # Fetch 'Profile' keyword files from the Chrome user data path
    profile_files = [f for f in os.listdir(chrome_user_data_path) if f.startswith('Profile')]
    if not profile_files:
        print(Fore.RED + "No 'Profile' keyword files found in the Chrome user data path.")
        return

    print(Fore.YELLOW + "Profile files available:")
    for idx, profile_file in enumerate(profile_files):
        print(f"{idx + 1}: {profile_file}")

    # Ask user to select a profile
    while True:
        try:
            choice = int(input("Enter the number of the profile to add auth token: "))
            if choice < 1 or choice > len(profile_files):
                print(Fore.RED + f"Invalid choice. Please enter a number between 1 and {len(profile_files)}.")
            else:
                selected_profile = profile_files[choice - 1]
                break
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.")

    # Ask user to input auth token
    profile_name = selected_profile.split('.')[0]  # Extract profile name from filename
    auth_token = input("Enter auth token: ").strip()

    # Validate auth token format
    if not is_valid_auth_token(auth_token):
        print(Fore.RED + "Invalid auth token format. Auth token must be 183 characters long and contain '.' after 36th character.")
        return

    # Save auth token to auth_profile.txt
    with open('auth_profile.txt', 'a') as f:
        f.write(f'{profile_name}: "{auth_token}"\n')

    print(Fore.GREEN + f"Auth token added successfully for profile '{profile_name}'.")


# Function to check if auth token format is valid
def is_valid_auth_token(auth_token):
    if len(auth_token) != 183:
        return False
    if auth_token[36] != '.':
        return False
    return True

# Function to show auth tokens from auth_profile.txt
def show_auth_tokens():
    print("\nAuth Tokens:")
    with open('auth_profile.txt', 'r') as f:
        for line in f:
            print(Fore.CYAN + line.strip())

# Function to start Selenium and run the script
def run_script():
    auth_profiles = load_auth_profiles()

    if not auth_profiles:
        print(Fore.RED + "No auth profiles found. Please add auth tokens first.")
        return

    num_iterations = int(input("Total Conversation to start: "))
    message = input("Enter the message to send: ")

    for profile_name, auth_token in auth_profiles:
        start_selenium(profile_name, auth_token, num_iterations, message)

# Function to load auth profiles from auth_profile.txt
def load_auth_profiles():
    auth_profiles = []
    with open('auth_profile.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                profile_name = parts[0].strip()
                auth_token = parts[1].strip().strip('"')
                auth_profiles.append((profile_name, auth_token))
    return auth_profiles

# Function to kill existing Chrome processes
def kill_existing_chrome_processes():
    for proc in psutil.process_iter():
        try:
            if proc.name() == 'chrome.exe':
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Function to send match request
def send_match_request(token):
    url = "https://api.chitchat.gg/match"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": f"token={token}"
    }
    data = {}  # Add any required data for the match request

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(Fore.GREEN + "Match request successful.")
    else:
        print(Fore.RED + f"Failed to send match request. Status code: {response.status_code}")
        return None

    return response.json()  # Return JSON response if needed

# Function to send message
def send_message(driver, message):
    try:
        message_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//textarea[@aria-label='Send a message']"))
        )
        message_box.clear()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        print(Fore.GREEN + f"Message '{message}' sent successfully.")
    except Exception as e:
        print(Fore.RED + f"Failed to send message: {str(e)}")

# Function to start Selenium with specified profile and auth token
def start_selenium(profile_name, auth_token, num_iterations, message):
    kill_existing_chrome_processes()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    webdriver_path = os.path.join(script_dir, 'chromedriver.exe')

    if not os.path.isfile(webdriver_path):
        raise FileNotFoundError(f"Chromedriver not found at path: {webdriver_path}")

    service = Service(webdriver_path)
    user_data_dir = get_saved_chrome_user_data_path()

    if not user_data_dir:
        print(Fore.RED + "Chrome user data path not found. Please update the path.")
        return

    options = Options()
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"profile-directory={profile_name}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://app.chitchat.gg/start/new')
        time.sleep(5)

        for i in range(num_iterations):
            match_response = send_match_request(auth_token)
            if not match_response:
                print(Fore.RED + "Exiting due to match request failure.")
                break
            time.sleep(5)

            send_message(driver, message)
            time.sleep(5)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def main():
    start_script()

if __name__ == "__main__":
    main()
