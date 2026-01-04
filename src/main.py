from argparse import ArgumentParser
import getpass
import asyncio
from typing import Literal, Any

from src.core.password_manager import PasswordManager
from src.core.clipboard_manager import ClipboardManager
from src.core.user_manager import UserManager
from src.logger import logger_config

def main(logger: Any, action: Literal["add", "remove", "update", "get"]) -> None:
    # Initializing managers
    user_manager = UserManager()
    logger.debug("UserManager initialized successfully")

    clipboard_manager = ClipboardManager()
    logger.debug("ClipboardManager initialized successfully")
    
    try:
        # Prompting the user for their credentials
        username = input("Enter your username: ")
        password = getpass.getpass(prompt="Enter your password: ")

        logger.info("Fetched user credentials successfully")

        # Attempting to register the user
        user_manager.register(username, password)

        # Logging user in
        if user_manager.login(username, password):
            # Initializing password manager
            password_manager = PasswordManager(username, password)
            valid_flag = False

            # Prompting the user for the entry details
            entry_name = input("Enter service name: ")
                
            match action:
                case "add":
                    password_1 = getpass.getpass(prompt="Enter service password: ")

                    while valid_flag is False:
                        # Prompting the user to confirm the password
                        password_2 = getpass.getpass(prompt="Enter service password again (type 'exit' to leave): ")

                        if password_2 == "exit":
                            logger.info("Exiting program")
                            return
                        if password_1 == password_2:
                            valid_flag = True

                    # Assuming entry name comes first and password comes second
                    password_manager.add_entry(entry_name, password_1)
                case "remove":
                    password_manager.remove_entry(entry_name)
                case "update":
                    password_1 = getpass.getpass(prompt="Enter service password: ")

                    while valid_flag is False:
                        # Prompting the user to confirm the password
                        password_2 = getpass.getpass(prompt="Enter service password again (type 'exit' to leave): ")

                        if password_2 == "exit":
                            logger.info("Exiting program")
                            return
                        if password_1 == password_2:
                            valid_flag = True

                    # Assuming entry name comes first and password comes second
                    password_manager.update_entry(entry_name, password_1)
                case "get":
                    res = password_manager.read_vault(entry_name)
                    
                    if (isinstance(res, str)):
                        asyncio.run(clipboard_manager.copy_to_clipboard(res))
                    else:
                        logger.error(f"Entry {entry_name} not found. Exiting program")
                        return
                case _:
                    logger.error("Invalid mode. Exiting program")
                    return
        else:
            logger.error("Login failed. Exiting program")
            raise
    except Exception as e:
        logger.error(e)
        return

if __name__ == "__main__":
    # Logger configuration
    logger = logger_config("main")

    parser = ArgumentParser(description="A simple, local password manager.")

    # Add arguments
    parser.add_argument("--add", "-a", action="store_true")
    parser.add_argument("--remove", "-rm", action="store_true")
    parser.add_argument("--update", "-u", action="store_true")
    parser.add_argument("--get", "-g", action="store_true")
    
    # Parse arguments
    args = parser.parse_args()

    if args.add == True:
        main(logger, "add")
    elif args.remove == True:
        main(logger, "remove")
    elif args.update == True:
        main(logger, "update")
    elif args.get == True:
        main(logger, "get")
    else:
        logger.error("Invalid argument. Exiting program")
        