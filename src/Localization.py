import gettext
import json
from pathlib import Path
from typing import Optional

# Root of the project (this file lives in <root>/src/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCALES_DIR = _PROJECT_ROOT / "locales"
DEFAULT_CONFIG_PATH = _PROJECT_ROOT / "config" / "config.json"

DOMAIN = "pyzelius"

# Languages available in the app. Keys are the codes used by gettext/locales
# folders, values are the language's own native name (shown as-is in menus,
# never translated).
SUPPORTED_LANGUAGES = {
    "en": "English",
    "it": "Italiano",
    "de": "Deutsch",
    "ru": "Русский",
}

DEFAULT_LANGUAGE = "it"


class Localization:
    """
    Centralizes language selection for the whole app using Python's
    built-in gettext module.

    Usage:
        Localization.install()          # loads saved/default language, installs `_`
        Localization.install("de")      # force a specific language
        Localization.set_language("ru") # persist choice to config.json

    Once installed, `_()` is available everywhere (builtins) without
    needing to import anything, exactly like the standard gettext workflow.
    """

    _current_lang: str = DEFAULT_LANGUAGE

    # ------------------------------------------------------------------
    # Setup / installation
    # ------------------------------------------------------------------

    @classmethod
    def install(cls, lang_code: Optional[str] = None, config_path: Optional[Path] = None) -> str:
        """
        Loads the requested language (or the saved/default one) and installs
        the `_()` gettext function globally. Returns the language code that
        actually got loaded.
        """
        config_path = config_path or DEFAULT_CONFIG_PATH
        lang_code = lang_code or cls.load_saved_language(config_path) or DEFAULT_LANGUAGE

        if lang_code not in SUPPORTED_LANGUAGES:
            lang_code = DEFAULT_LANGUAGE

        try:
            translation = gettext.translation(
                DOMAIN, localedir=str(LOCALES_DIR), languages=[lang_code]
            )
        except FileNotFoundError:
            # Falls back to the raw msgids (used as the source strings).
            translation = gettext.NullTranslations()

        translation.install()
        cls._current_lang = lang_code
        return lang_code

    @classmethod
    def get_language(cls) -> str:
        return cls._current_lang

    @classmethod
    def get_language_name(cls, lang_code: Optional[str] = None) -> str:
        lang_code = lang_code or cls._current_lang
        return SUPPORTED_LANGUAGES.get(lang_code, lang_code)

    # ------------------------------------------------------------------
    # Persistence (reuses config.json, same file Pathfinder writes to)
    # ------------------------------------------------------------------

    @staticmethod
    def load_saved_language(config_path: Optional[Path] = None) -> Optional[str]:
        config_path = Path(config_path or DEFAULT_CONFIG_PATH)
        if not config_path.exists():
            return None
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("language")
        except (json.JSONDecodeError, OSError):
            return None

    @staticmethod
    def save_language(lang_code: str, config_path: Optional[Path] = None) -> None:
        config_path = Path(config_path or DEFAULT_CONFIG_PATH)
        data = {}
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                data = {}

        data["language"] = lang_code

        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def set_language(cls, lang_code: str, config_path: Optional[Path] = None) -> None:
        """
        Persists the chosen language for the next launch. Since Tkinter
        widgets don't retranslate themselves live, the app needs to be
        restarted for the change to take full effect (see
        ControllerV3.restart_app).
        """
        if lang_code not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language '{lang_code}'.")
        cls.save_language(lang_code, config_path)
