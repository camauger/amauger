import yaml
import json
from pathlib import Path
import logging
import glob


class ConfigLoader:
    def __init__(self, src_path: Path):
        self.src_path = src_path

    def load_translations(self):
        """
        Load translations from JSON files organized by language and namespace.
        Returns a nested dictionary structure:
        {
            "en": {
                "common": {...},
                "blog": {...},
                ...
            },
            "fr": {
                "common": {...},
                "blog": {...},
                ...
            }
        }
        """
        translations = {}
        translations_dir = self.src_path / 'data' / 'translations'

        # Check if we're still using the old YAML format
        old_yaml_path = self.src_path / 'data' / 'translations.yaml'
        if old_yaml_path.exists():
            logging.warning(
                "Using legacy translations.yaml file. Consider migrating to JSON format.")
            with open(old_yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)

        # Load from new JSON structure
        if not translations_dir.exists():
            logging.error(
                f"Translations directory not found at {translations_dir}")
            return {}

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
                except json.JSONDecodeError as e:
                    logging.error(f"Error loading {json_file}: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error loading {json_file}: {e}")

        # Flatten the structure for backward compatibility
        return self._flatten_translations(translations)

    def _flatten_translations(self, nested_translations):
        """
        Flattens the nested translations structure to maintain backward compatibility
        with the existing codebase.
        """
        flattened = {}
        for lang, namespaces in nested_translations.items():
            flattened[lang] = {}
            for namespace, translations in namespaces.items():
                flattened[lang].update(translations)
        return flattened

    def load_projects(self):
        with open(self.src_path / 'data' / 'projects.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_site_config(self):
        with open(self.src_path / 'config' / 'site_config.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
