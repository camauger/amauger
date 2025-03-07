from pathlib import Path
import json
import logging
import re
from typing import Dict, Any

try:
    from pyicumessageformat import MessageFormat
    HAS_ICU = True
except ImportError:
    HAS_ICU = False
    logging.warning("pyicumessageformat is not installed. ICU MessageFormat will not be available. "
                   "Install with: pip install pyicumessageformat")

class TranslationManager:
    def __init__(self, translations: Dict[str, Dict[str, Any]], default_lang: str = 'en'):
        self.translations = translations
        self.default_lang = default_lang
        self.message_formatters = {}
        
        # Initialize formatters for each language if ICU is available
        if HAS_ICU:
            for lang in translations.keys():
                self.message_formatters[lang] = MessageFormat(locale=lang)
    
    def get(self, key: str, lang: str, params: Dict[str, Any] = None) -> str:
        """
        Get a translation value with ICU MessageFormat support.
        
        Args:
            key: The translation key (can contain dots for namespaced keys)
            lang: The language code
            params: Optional parameters for MessageFormat
            
        Returns:
            The translated string
        """
        # Fall back to default language if requested language not available
        if lang not in self.translations:
            lang = self.default_lang
            
        # Get the nested value based on dot notation (e.g., "blog.read_more")
        value = self._get_nested_value(self.translations.get(lang, {}), key)
        
        # If value not found in requested language, try default language
        if value is None and lang != self.default_lang:
            value = self._get_nested_value(self.translations.get(self.default_lang, {}), key)
            
        # Still not found, return the key as fallback
        if value is None:
            return key
            
        # Return as is if no params or ICU not available
        if params is None or not HAS_ICU:
            return value
            
        # Format message with ICU
        try:
            formatter = self.message_formatters.get(lang)
            if formatter:
                return formatter.format(value, params)
            return value
        except Exception as e:
            logging.error(f"Error formatting message '{value}' with params {params}: {e}")
            return value
    
    def _get_nested_value(self, data: Dict[str, Any], key: str) -> Any:
        """
        Get a nested value from a dictionary using dot notation.
        Example: get_nested_value({"blog": {"title": "My Blog"}}, "blog.title") -> "My Blog"
        """
        parts = key.split('.')
        
        # Handle non-namespaced legacy structure
        if len(parts) == 1:
            return data.get(key)
            
        # Handle namespaced keys
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current
        
    @classmethod
    def from_directory(cls, translations_dir: Path, default_lang: str = 'en') -> 'TranslationManager':
        """
        Load translations from a directory structure.
        
        Args:
            translations_dir: Path to translations directory
            default_lang: Default language code
            
        Returns:
            A TranslationManager instance
        """
        translations = {}
        
        # Process each language directory
        for lang_dir in translations_dir.glob('*'):
            if not lang_dir.is_dir():
                continue
                
            lang = lang_dir.name
            translations[lang] = {}
            
            # Load each namespace file
            for json_file in lang_dir.glob('*.json'):
                try:
                    namespace = json_file.stem
                    with open(json_file, 'r', encoding='utf-8') as f:
                        translations[lang][namespace] = json.load(f)
                except Exception as e:
                    logging.error(f"Error loading {json_file}: {e}")
        
        return cls(translations, default_lang)
