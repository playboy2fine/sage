import shutil
import logging
import traceback

from datetime import datetime
from typing import Optional

from logging import (
    Logger as LoggingLogger,
    Formatter, FileHandler, StreamHandler,
    INFO, ERROR, CRITICAL, DEBUG,
    getLogger
)

from .helpers import format_exception
from .config import config
from .paths import paths


class LoggingFormatter(Formatter):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLOURS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold
    }

    def format(self, record):
        log_color = self.COLOURS.get(record.levelno)

        format_str = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format_str = format_str.replace("(black)", self.black + self.bold)
        format_str = format_str.replace("(reset)", self.reset)
        format_str = format_str.replace("(levelcolor)", log_color)  # type: ignore
        format_str = format_str.replace("(green)", self.green + self.bold)

        formatter = logging.Formatter(format_str, "%d-%m-%y %H:%M:%S", style="{")

        return formatter.format(record)


latest_log_dirname = paths.log_latest.parent

if paths.log_latest.exists():
    try:
        creation_time = paths.log_latest.stat().st_ctime
        old_timestamp = datetime.fromtimestamp(creation_time).strftime("%d.%m.%y-%H%M%S")

        paths.log_latest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(paths.log_latest, paths.log_history.joinpath(f"sage-{old_timestamp}.log"))

    except FileNotFoundError:
        paths.log_latest.unlink(True)

console_handler = StreamHandler()
console_handler.setFormatter(LoggingFormatter())

file_handler = FileHandler(paths.log_latest, mode="a", encoding="utf-8", delay=False)
file_handler.setFormatter(
    Formatter(
        "[{asctime}] [{levelname:<8s}] {name}: {message}", "%d.%m.%y %H:%M:%S",
        style="{"
    )
)


class Logger:
    ROOT: LoggingLogger = getLogger("Sage")
    TESTS: LoggingLogger = getLogger("Tests")
    ERRORS: LoggingLogger = getLogger("Errors")
    UTILS: LoggingLogger = getLogger("Utils")
    LOCALE: LoggingLogger = getLogger("Locale")


handlers = [console_handler, file_handler]

for l_name, l_obj in vars(Logger).items():
    if isinstance(l_obj, LoggingLogger):
        l_obj.setLevel(DEBUG if config.debug else INFO)

        for handler in handlers:
            l_obj.addHandler(handler)


def log_exception(
        e: Exception,
        logger: Optional[LoggingLogger] = None,
        critical: bool = False,
        save_trace: bool = True
) -> str:
    formatted = format_exception(e)
    level = CRITICAL if critical else ERROR

    if not logger:
        logger = Logger.ROOT

    logger.log(level, formatted)

    if save_trace:
        trace = traceback.format_exception(type(e), e, e.__traceback__)
        trace = "".join(trace)

        now = datetime.now().strftime("%d.%m.%y-%H%M%S")
        filename = f"{type(e).__name__}_{now}.txt"
        filepath = paths.log_tracebacks.joinpath(filename)

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(trace)

    return formatted