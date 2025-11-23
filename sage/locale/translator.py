import os

from discord import Locale
from typing import Optional

from discord.app_commands import locale_str, Translator as DiscordTranslator, TranslationContextTypes

from ..paths import paths
from .manager import get_string

SUPPORTED_LOCALES = [p.split(".")[0] for p in os.listdir(paths.locale)]


class Translator(DiscordTranslator):
    async def translate(
            self,
            string: locale_str,
            locale: Locale,
            context: TranslationContextTypes
    ) -> Optional[str]:
        key = string.message if isinstance(string, locale_str) else string

        if not key:
            return ""

        if locale == Locale.american_english:
            locale = Locale.british_english

        return get_string(locale, key)