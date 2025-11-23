import sys
import yaml

from pathlib import Path
from typing import TypeVar
from pydantic import BaseModel, Field, ValidationError

from .paths import paths

T = TypeVar("T", bound=BaseModel)


class _ConfigStatus(BaseModel):
    language: str
    interval: int
    log: bool


class Config(BaseModel):
    version: str
    debug: bool
    timestamp_format: str
    forward_discord_logs: bool
    always_sync_command_tree: bool
    status: _ConfigStatus
    internal_extensions: list[str] = Field(default_factory=list)
    intents: dict[str, bool] = Field(default_factory=dict)


def config_model_factory(path: Path, model: type[T]) -> T:
    if not path.exists():
        sys.exit(f"File not found at {str(path)}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            return model(**yaml.safe_load(f))
        except (ValidationError, yaml.YAMLError) as e:
            sys.exit(f"Failed to parse {str(path)}: {str(e)}")
        except Exception as e:
            sys.exit(f"Unexpected error while loading {str(path)}: {str(e)}")


config = config_model_factory(paths.config, Config)