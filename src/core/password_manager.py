import nacl.secret
import nacl.utils
import nacl.pwhash
import json, os
from typing import Optional, Dict, Any, Tuple
from logger import logger_config
from dotenv import load_dotenv
load_dotenv()

class PasswordManager():
    def __init__(self, username: str, password: str) -> None:
        # Configure logger
        self.logger = logger_config("PasswordManager")

        # Get vault and key directories from .env
        vault_dir = os.getenv("VAULT_DIR")
        key_dir = os.getenv("KEY_DIR")
        
        # Initialize vault path
        self.vault_base_path = f"{vault_dir if vault_dir else "."}/.vaults/.{username}/vault/"
        self.vault_path = os.path.join(self.vault_base_path, "secret.json")

        # Configure encryption
        self.key_path = os.path.join(key_dir if key_dir else self.vault_base_path, "key.bin")
        self.key = self._load_or_create_key(password)
        self.box = nacl.secret.SecretBox(self.key)

        # Initialize vault
        self.logger.info("Initializing vault")
        if not os.path.exists(self.vault_path):
            self._initialize_vault()
        self.logger.info("Vault initialized successfully")
    
    def _initialize_vault(self) -> None:
        try:
            # Ensure parent directory exists
            parent_dir = os.path.dirname(self.vault_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            encrypted = self.box.encrypt(json.dumps({}).encode("utf-8"))

            # Create vault
            with open(self.vault_path, mode="wb") as vault:
                vault.write(encrypted)
        except Exception as e:
            self.logger.error(f"Error initializing vault: {e}")

    def read_vault(self, entry_name: Optional[str] = None) -> Dict[str, Any] | None:
        try:
            # Reading vault
            with open(self.vault_path, mode="rb") as vault:
                encrypted = vault.read()
                decrypted = self.box.decrypt(encrypted)
                data = json.loads(decrypted.decode("utf-8"))

            return data if not entry_name else data.get(entry_name, None)
        except Exception as e:      
            self.logger.error(f"Error reading vault: {e}")
    
    def add_entry(self, entry_name: str, password: str, additional_info: Optional[Dict[str, str]] = None) -> None:
        try:
            # Read vault
            vault_data = self.read_vault()
            if not vault_data or not isinstance(vault_data, dict):
                vault_data = {}

            # Add entry
            if (vault_data.get(entry_name, None) != None):
                raise Exception("Entry already exists")
            

            vault_data[entry_name] = {
                "password": password, 
                "additional_info": additional_info if additional_info else {}
            }

            # Persist changes
            encrypted = self.box.encrypt(json.dumps(vault_data).encode("utf-8"))
            with open(self.vault_path, mode="wb") as vault:
                vault.write(encrypted)

            self.logger.info(f"Entry {entry_name} added successfully")
        except Exception as e:
            self.logger.error(f"Error adding entry: {e}")

    def remove_entry(self, entry_name: str) -> None:
        try:
            # Read vault
            vault_data = self.read_vault()
            if not vault_data:
                self.logger.error("Vault is empty")
                return
            
            # Remove entry
            removed_entry = vault_data.pop(entry_name, None)
            self.logger.info(f"Entry {removed_entry} removed successfully")

            # Persist changes
            encrypted = self.box.encrypt(json.dumps(vault_data).encode("utf-8"))
            with open(self.vault_path, mode="wb") as vault:
                vault.write(encrypted)

            self.logger.info(f"Entry {entry_name} removed successfully")
        except Exception as e:
            self.logger.error(f"Error removing entry: {e}")
    
    def update_entry(self, entry_name: str, update_info: Dict[str, Any]) -> None:
        try:
            # Read vault
            vault_data = self.read_vault()
            if not vault_data:
                self.logger.error("Vault is empty")
                return
            
            # Check if any info has been provided
            if not update_info:
                self.logger.error("No new info has been provided")
            
            # Handle entry rename if "entry_name" is in update_info
            new_entry_name = update_info.pop("entry_name", None)
            if new_entry_name:
                if new_entry_name in vault_data:
                    raise ValueError(f"Entry '{new_entry_name}' already exists")
                vault_data[new_entry_name] = vault_data.pop(entry_name)
                entry_name = new_entry_name  # Update reference for further updates
            
            # Update other fields
            entry = vault_data[entry_name]
            for key, value in update_info.items():
                if key == "password":
                    entry["password"] = value
                else:
                    # Assume other keys are in additional_info
                    entry["additional_info"][key] = value
                  
            # Persist changes
            encrypted = self.box.encrypt(json.dumps(vault_data).encode("utf-8"))
            with open(self.vault_path, mode="wb") as vault:
                vault.write(encrypted)
            
            self.logger.info(f"Entry {entry_name} updated successfully")
        except Exception as e:
            self.logger.error(f"Error updating entry: {e}")

    def _load_or_create_key(self, password: str) -> bytes:
        # Check if a key exists in the user's path
        if not os.path.exists(self.key_path):
            # Salt
            salt_size = nacl.pwhash.argon2i.SALTBYTES
            salt = nacl.utils.random(salt_size)

            # Creating key
            # Using KDF to create a key based on the user's password
            key = nacl.pwhash.argon2i.kdf(32, password.encode(), salt)

            # Getting parent directory
            parent_dir = os.path.dirname(self.key_path)

            # Write to file
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            with open(self.key_path, "wb") as f:
                f.write(key)
            return key
        else:
            # Get key from file
            with open(self.key_path, "rb") as f:
                return f.read()



    

    