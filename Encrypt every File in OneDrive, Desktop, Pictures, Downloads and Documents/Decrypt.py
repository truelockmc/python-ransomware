import os
import base64
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet

def decrypt_file(file_path, fernet):
    """Decrypts a single file."""
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)
        
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        return True
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")
        return False

def walk_and_decrypt(directory, fernet):
    """Walks through the directory and decrypts all files."""
    file_count = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        # Decrypt all files in the current directory
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if decrypt_file(file_path, fernet):
                file_count += 1

    return file_count

def get_user_folders():
    """Returns the paths to the user's Desktop, Documents, Downloads, and OneDrive folders."""
    user_profile = os.environ['USERPROFILE']  # Get the path to the user's profile directory
    desktop_folder = os.path.join(user_profile, "Desktop")
    documents_folder = os.path.join(user_profile, "Documents")
    downloads_folder = os.path.join(user_profile, "Downloads")
    onedrive_folder = os.path.join(user_profile, "OneDrive")
    picture_folder = os.path.join(user_profile, "Pictures")
    
    return [desktop_folder, documents_folder, downloads_folder, onedrive_folder, picture_folder]

def ask_for_key():
    """Displays a dialog to ask the user for the decryption key."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    key = simpledialog.askstring("Decrypt", "Please enter the decryption key:")
    return key

def main():
    # Ask the user for the decryption key
    key = ask_for_key()
    
    if not key:
        print("No key provided. Exiting...")
        return

    # Decode the key
    try:
        key_bytes = base64.urlsafe_b64decode(key)
        fernet = Fernet(key_bytes)
    except Exception as e:
        print(f"Invalid key format: {e}")
        return

    # Get the list of user folders to decrypt
    user_folders = get_user_folders()

    total_files = 0

    # Decrypt all files in each folder
    for folder in user_folders:
        if os.path.exists(folder):
            files_decrypted = walk_and_decrypt(folder, fernet)
            total_files += files_decrypted

    # Notify the user about the decryption result
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Decryption Complete", f"Total files decrypted: {total_files}")

if __name__ == "__main__":
    main()
