import structlog
import logging
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

def logger_config(process_name: Optional[str], pretty: Optional[bool] = True):
    """
    Configure the logger to use structlog with optional pretty-print output.

    :param pretty: Whether to enable pretty-printing for logs.
    """
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        level = "INFO"
        raise ValueError(f"Invalid LOG_LEVEL: {level}. Must be one of the following: DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaulting to INFO.")
    
    logging.basicConfig(level=level)

    processors = [
        structlog.processors.TimeStamper(fmt="iso"),  # Add timestamp to logs
        structlog.dev.ConsoleRenderer() if pretty else structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger()
    if process_name:
        logger = logger.bind(process=process_name)

    return logger