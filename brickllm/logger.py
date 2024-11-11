import logging

# Create custom log level
EURAC_LEVEL = 25
logging.addLevelName(EURAC_LEVEL, "EURAC")


def eurac(self, message, *args, **kwargs):
    """
    Log with custom EURAC level
    """
    if self.isEnabledFor(EURAC_LEVEL):
        self._log(EURAC_LEVEL, message, args, **kwargs)


# Add eurac method to Logger class
logging.Logger.eurac = eurac


# Create and configure logger
def get_logger(name="BrickLLM"):
    logger = logging.getLogger(name)

    # Create handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(EURAC_LEVEL)
    return logger


# Create default logger instance
custom_logger = get_logger()
