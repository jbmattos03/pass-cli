import pyperclip
import asyncio
from logger import logger_config

class ClipboardManager():
    """
    Class for managing clipboard functionalities.
    """
    def __init__(self, n: int = 10) -> None:
        # This attribute informs whether an item is currently copied to the clipboard
        self.active = False

        # Time item is available in the clipboard before being deleted
        self.clipboard_time = n

        # Logger
        self.logger = logger_config("ClipboardManager")

    def _paste_from_clipboard(self) -> str:
        return pyperclip.paste()
    
    async def count_n_seconds(self):
        """
        Function to count n seconds asynchronously.
        """
        seconds = self.clipboard_time

        while seconds > 0:
            self.logger.info(f"Counting down from {self.clipboard_time}: {seconds} remaining")
            await asyncio.sleep(1) # Asynchronously sleep for 1s

            seconds -= 1
        
        self.logger.info("Countdown finished")

    async def copy_to_clipboard(self, string: str) -> None:
        # Activate ClipboardManager
        self.active = True

        # Save current clipboard content
        current_content = self._paste_from_clipboard()
        self.logger.debug(f"Current clipboard content: {current_content}")

        # Copy updated content to clipboard
        self.logger.info("Copying content to clipboard")
        pyperclip.copy(string)

        # Wait 10 seconds
        await self.count_n_seconds()

        # Delete content from clipboard
        self._delete_from_clipboard(current_content)

        # Deactivate ClipboardManager
        self.active = False

    def _delete_from_clipboard(self, last_content: str):
        pyperclip.copy(last_content)
        self.logger.info("Deleted string from clipboard successfully")