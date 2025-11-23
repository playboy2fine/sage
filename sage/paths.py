import sys

from pathlib import Path
from dataclasses import dataclass, field

from .helpers import get_path


@dataclass
class Paths:
    root: Path = field(default_factory=lambda: get_path("."))

    config: Path = field(default_factory=lambda: get_path("config/sage_client.yml"))
    locale: Path = field(default_factory=lambda: get_path("assets/locale"))

    data: Path = field(default_factory=lambda: get_path("/var/sage/data", True))
    temp: Path = field(default_factory=lambda: get_path("/var/sage/data/temp", True))

    log_latest: Path = field(default_factory=lambda: get_path("/var/sage/logs/latest.log", True))
    log_history: Path = field(default_factory=lambda: get_path("/var/sage/logs/history", True))
    log_tracebacks: Path = field(default_factory=lambda: get_path("/var/sage/logs/tracebacks", True))

    def __post_init__(self) -> None:
        exceptions = [
            "log_latest"
        ]

        missing = []

        for f in self.__dataclass_fields__:  # type: ignore
            if f not in exceptions and not getattr(self, f).exists():
                missing.append(f)

        if missing:
            sys.exit(f"Initialization failed, required paths are missing: {', '.join(missing)}")


paths = Paths()