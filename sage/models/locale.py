from dataclasses import dataclass, fields


@dataclass
class Localisation:
    statuses: dict[str, list[str]]
    states: dict[str, str]
    ui: dict[str, str]
    errors: dict[str, str]
    commands: dict[str, str | list[str]]

    def get(self, key: str, default: str | list[str]) -> str | list[str]:
        merged = {}

        for field in fields(self):
            merged.update(getattr(self, field.name))

        return merged.get(key, default)