import logging


def parse_frontmatter(content: str):
    """
    Analyse le front matter d'un fichier Markdown.
    Renvoie un tuple (metadata, markdown_content).
    """
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            _, frontmatter, markdown_content = parts
            metadata = {}
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    if key.strip() in ['categories', 'meta_keywords']:
                        try:
                            value = value.strip().strip('[]').split(',')
                            value = [v.strip() for v in value if v.strip()]
                        except Exception as e:
                            logging.error(
                                f"Erreur lors du parsing de {key}: {e}")
                            value = []
                    else:
                        value = value.strip()
                    metadata[key.strip()] = value
            return metadata, markdown_content
    return {}, content
