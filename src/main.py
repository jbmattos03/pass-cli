from argparse import ArgumentParser
import getpass
import asyncio
from typing import Literal, Any
from pprint import pprint

from core.password_manager import PasswordManager
from core.clipboard_manager import ClipboardManager
from core.user_manager import UserManager
from logger import logger_config

def main(logger: Any, action: Literal["add", "remove", "update", "get", "show"]) -> None:
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
            logger.debug("PasswordManager initialized successfully")

            # Prompting the user for the entry details
            entry_name = input("Enter service name: ")

            valid_flag = False
            options = {}
            
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

                    options_question = input("Do you want to add any additional information (eg.: username, email, etc.)?\nType 'y' for yes or 'n' for no. ")
                    if options_question == "y":
                        while True:
                            option_name = input("Enter option name (ex.: username). Type ':wq' to stop: ")
                            if (option_name == ":wq"):
                                logger.info(f"Options collected successfully for entry {entry_name}")
                                break

                            option_value = input("Enter option value: ")
                        

                            options[option_name] = option_value

                    # Assuming entry name comes first and password comes second
                    password_manager.add_entry(entry_name, password_1, options)
                case "remove":
                    password_manager.remove_entry(entry_name)
                case "update":
                    attributes = {}

                    while True:
                        attribute_name = input("Enter attribute name (eg.: username). Type ':wq' to stop: ")
                        if (attribute_name == ":wq"):
                            logger.info(f"Options collected successfully for entry {entry_name}")
                            break

                        attribute_value = input("Enter option value: ")
                    

                        attributes[attribute_name] = attribute_value

                    # Assuming entry name comes first and password comes second
                    password_manager.update_entry(entry_name, attributes)
                case "get":
                    res = password_manager.read_vault(entry_name)
                    if res is None:
                        logger.error(f"Entry {entry_name} not found. Exiting program")
                        return
                    
                    password = res["password"]
                    logger.debug(f"{password}")
                    
                    if password is not None:
                        asyncio.run(clipboard_manager.copy_to_clipboard(password))
                    else:
                        logger.error(f"Key 'password' not found for entry {entry_name}. Exiting program")
                        return
                case "show":
                    res = password_manager.read_vault(entry_name)
                    if res is None:
                        logger.error(f"Entry {entry_name} not found. Exiting program")
                        return
                    
                    # Printing whole entry or remove password
                    password_question = input("WARNING: Echoing your entry's sensitive information to the terminal could pose a security risk.\nIt is advisable to run this program with --get flag to access your entry's sensitive information.\nWould you like to remove the password from the display? Type 'y' for yes or 'no' for no. """)
                    
                    if password_question == "y":
                        del res["password"]
                    
                    pprint(res, indent=4)
                case _:
                    logger.error("Invalid mode. Exiting program")
                    return
        else:
            logger.error("Login failed. Exiting program")
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
    parser.add_argument("--show", "-s", action="store_true")
    
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
    elif args.show == True:
        main(logger, "show")
    else:
        logger.error("Invalid argument. Exiting program")
        