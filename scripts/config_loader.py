import yaml
from pathlib import Path


class ConfigLoader:
    def __init__(self, src_path: Path):
        self.src_path = src_path

    def load_translations(self):
        with open(self.src_path / 'data' / 'translations.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_projects(self):
        with open(self.src_path / 'data' / 'projects.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_site_config(self):
        with open(self.src_path / 'config' / 'site_config.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
