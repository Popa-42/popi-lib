import logging
from typing import Literal
from datetime import datetime

class ColorCodes:
    GRAY = "\x1b[37m"
    WHITE = "\x1b[97m"
    YELLOW = "\x1b[38;5;220m"
    RED = "\x1b[31m"
    BOLD_RED = "\x1b[31;1m"
    BOLD_STRONG_RED = "\x1b[91;1m"
    BOLD_GREEN = "\x1b[01;32m"
    BOLD_YELLOW = "\x1b[01;38;5;226m"
    RESET = "\x1b[0m"
    RESET_WEIGHT = "\x1b[22m"

class CustomFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%d %H:%M"
    _fmt = "{message}"

    FORMATS = {
        logging.DEBUG: f"\033[38;5;30m[{{asctime}}] {ColorCodes.GRAY + '{levelname:>8s}' + ColorCodes.RESET_WEIGHT}: " + _fmt + ColorCodes.RESET,
        logging.INFO: f"\033[38;5;44m[{{asctime}}] {ColorCodes.BOLD_GREEN + '{levelname:>8s}' + ColorCodes.RESET_WEIGHT}: " + ColorCodes.WHITE + _fmt + ColorCodes.RESET,
        logging.WARNING: f"\033[38;5;44m[{{asctime}}] {ColorCodes.BOLD_YELLOW + '{levelname:>8s}' + ColorCodes.RESET_WEIGHT}: " + ColorCodes.YELLOW + _fmt + ColorCodes.RESET,
        logging.ERROR: f"\033[38;5;44m[{{asctime}}] {ColorCodes.BOLD_RED + '{levelname:>8s}' + ColorCodes.RESET_WEIGHT}: " + _fmt + ColorCodes.RESET,
        logging.CRITICAL: f"\033[01;38;5;203m[{{asctime}}] {ColorCodes.BOLD_STRONG_RED + '{levelname:>8s}'}: " + _fmt + ColorCodes.RESET
    }

    def __init__(self, style: Literal["%", "{", "$"] = "{", datefmt: str = default_time_format):
        super().__init__(style=style, datefmt=datefmt)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime(self.default_time_format)

    def format(self, record):
        if not hasattr(record, 'asctime'):
            record.asctime = self.formatTime(record, self.datefmt)
        log_fmt = self.FORMATS.get(record.levelno, self._fmt)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt, style='{')
        return formatter.format(record)

class CustomLogger(logging.Logger):
    def __init__(self, name: str = __name__, debug: bool = False) -> None:
        super().__init__(name)
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        self.addHandler(handler)
        self.setLevel(logging.DEBUG if debug else logging.INFO)

if __name__ == "__main__":
    logger = CustomLogger(debug=True)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning.")
    logger.error("This is an error message.")
    logger.critical("This is a critical error message!")
