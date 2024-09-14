import os
import base64
import tkinter as tk
from tkinter import simpledialog
from cryptography.fernet import Fernet

def decrypt_file(file_path, key):
    """Decrypts a single file."""
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)
        
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print(f"Decrypted: {file_path}")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

def walk_and_decrypt(directory, key):
    """Walks through the directory and decrypts all files."""
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            decrypt_file(file_path, key)

def get_key_from_user():
    """Displays a popup to get the decryption key from the user."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    key_input = simpledialog.askstring("Decrypt your Files", "Please enter your decryption key:")
    if key_input:
        try:
            # Decode the Base64 encoded key
            key = base64.urlsafe_b64decode(key_input.encode())
            return key
        except Exception as e:
            print(f"Invalid key format. Error: {e}")
            return None
    else:
        print("No key entered.")
        return None

def main():
    # Get the decryption key from the user
    key = get_key_from_user()
    
    if key:
        # Use the current directory as the starting point for decryption
        current_directory = os.getcwd()
        
        # Decrypt all files in the current directory and subdirectories
        walk_and_decrypt(current_directory, key)
    else:
        print("Decryption aborted due to invalid key.")

if __name__ == "__main__":
    main()
