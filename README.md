# Python Ransomware

This repository contains Python scripts designed for encrypting and decrypting files on a Windows system. The ransomware scripts encrypt files in specific user directories and provide a method for decryption. The Ransomware also bypasses Microsoft Defender with adding itself as an Exclusion.

**Disclaimer**: This software is provided for educational purposes only. Unauthorized use of these scripts can result in legal consequences and significant data loss. Always use such tools ethically and responsibly.

## Contents

1. **Ransomware.py**: Encrypts files in specified user directories and sends encryption details to a Discord webhook.
2. **Decrypt.py**: Decrypts files encrypted by the ransomware.

## Files

### Ransomware.py

This script performs the following actions:
- Generates an encryption key.
- Encrypts all files in the user's Desktop, Documents, Downloads, OneDrive, and Pictures directories.
- Sends encryption details (key, file count, folder count) to a Discord webhook.
- Displays a notification with the path to a file containing an identifier code.

**Dependencies**:
- `cryptography`
- `requests`
- `tkinter`

**Usage**:
1. Replace `YOUR_WEBHOOK_URL` with your Discord webhook URL in the script.
2. Run the script with administrator privileges to encrypt files.

```bash
python Ransomware.py
```

### Decrypt.py

This script is used to decrypt files encrypted by `Ransomware.py`. It:
- Prompts the user for the decryption key.
- Decrypts all files in the current directory and its subdirectories.

**Dependencies**:
- `cryptography`
- `tkinter`

**Usage**:
1. Run the script and provide the decryption key when prompted.

```bash
python Decrypt.py
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies**

   ```bash
   pip install cryptography requests
   ```

3. **Run the Ransomware**

   ```bash
   python Ransomware.py
   ```

   Ensure you have replaced the placeholder in the script with your actual Discord webhook URL.

4. **Decrypt Files**

   ```bash
   python Decrypt.py
   ```

   Enter the decryption key when prompted.

## Important Notes

- **Ethical Use**: These scripts are intended for educational purposes. Unauthorized encryption of files can lead to legal consequences and data loss.
- **Backup**: Always ensure that you have backups of important data before running encryption or decryption scripts.
- **Testing**: Test in a controlled environment to avoid accidental data loss.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or concerns, please contact [anonyson@proton.me](mailto:anonyson@proton.me).

---

**Disclaimer**: The authors of this project are not responsible for any damages or legal consequences resulting from the use or misuse of these scripts.
