import json
import os
from typing import Optional
from logger import logger_config
from core.password_utils import *

class UserManager:
    """
    Class for managing users in a user base.
    """
    def __init__(self, userfile_path: Optional[str] = None):
        # Logger config
        self.logger = logger_config("UserManager")

        # Initialize userfile path
        self.userfile_path = userfile_path if userfile_path else f"./.users/users.json"

        # Initialize userfile
        if not os.path.exists(self.userfile_path):
            self._initialize_userfile()

    def _initialize_userfile(self) -> None:
        try:
            # Ensure parent directory exists
            parent_dir = os.path.dirname(self.userfile_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            # Creating 
            with open(self.userfile_path, mode="w", encoding="utf-8") as userfile:
                json.dump({}, userfile, indent=4)
        except Exception as e:
            self.logger.error(f"Error initializing userfile: {e}")

    def register(self, username: str, password: str) -> None:
        try:
            # Read userfile
            with open(self.userfile_path, mode="r", encoding="utf-8") as userfile:
                userfile_data = json.load(userfile)
            
            # Add entry
            if userfile_data.get(username, None) != None:
                self.logger.error("Username taken")
                return
            
            # Add hashed password to json file
            userfile_data[username] = hash_password(password)

            # Persist changes
            with open(self.userfile_path, mode="w", encoding="utf-8") as userfile:
                json.dump(userfile_data, userfile, indent=4)
        except Exception as e:
            self.logger.error(f"Error registering user: {e}")

    def login(self, username: str, password: str) -> bool | None:
        try:
            # Read userfile
            with open(self.userfile_path, mode="r", encoding="utf-8") as userfile:
                userfile_data = json.load(userfile)
            
            # Get hashed password
            user_password = userfile_data.get(username, None)
            if (user_password is None):
                self.logger.error(f"No entry found for username {username}")
                return
                
            return compare(user_password, password)
        except Exception as e:
            self.logger.error(f"Error logging user in: {e}")
        
