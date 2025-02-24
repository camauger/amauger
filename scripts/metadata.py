import logging
import yaml


def extract_metadata(content: str) -> dict:
    """Extrait les métadonnées d'un contenu Markdown en utilisant le front matter YAML."""
    try:
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1]) or {}
                metadata.setdefault('categories', [])
                metadata.setdefault('meta_keywords', [])
                if not isinstance(metadata['categories'], list):
                    metadata['categories'] = [metadata['categories']]
                if not isinstance(metadata['meta_keywords'], list):
                    metadata['meta_keywords'] = [metadata['meta_keywords']]
                return metadata
    except yaml.YAMLError as e:
        logging.error(f"Erreur YAML lors de l'extraction des métadonnées: {e}")
    except Exception as e:
        logging.error(
            f"Erreur générale lors de l'extraction des métadonnées: {e}")
    return {}
