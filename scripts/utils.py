from babel.dates import format_date
from datetime import datetime, date
from unidecode import unidecode
import frontmatter
import markdown
import re


def markdown_filter(text):
    """Convertit le texte Markdown en HTML."""
    return markdown.markdown(text, extensions=['meta'])


def build_page(content, template_name, lang, custom_url, is_post, slug,
               translations, site_config, projects, jinja_env, content_translations=None, pagination=None):
    """Génère une page HTML en utilisant Jinja."""

    # Charger une seule fois le contenu et les métadonnées
    parsed = frontmatter.loads(content)
    metadata = parsed.metadata
    md_content = parsed.content
    html_content = markdown_filter(md_content)

    # Déterminer l'URL de la page en fonction du type
    if is_post:
        effective_slug = slug if slug is not None else metadata.get(
            'slug', 'post')
        blog_path = site_config['blog_url'].strip('/')
        if site_config.get("unilingual"):
            page_url = f"/{blog_path}/{effective_slug}/"
        else:
            page_url = f"/{lang}/{blog_path}/{effective_slug}/"
    elif custom_url is not None:
        page_url = custom_url
    else:
        page_url = "/" if site_config.get("unilingual") else f"/{lang}/"

    # Toujours inclure `pagination` même si elle est vide
    if pagination is None:
        pagination = {'posts': []}

    # Construire le contexte de la page
    page_metadata = {
        'lang': lang,
        'url': page_url,
        'content_translations': content_translations if content_translations is not None else {},
        'pagination': pagination,
        **metadata
    }

    # Rendu avec Jinja
    template = jinja_env.get_template(template_name)
    return template.render(
        content=html_content,
        page=page_metadata,
        t=translations,
        site=site_config,
        projects=projects
    )


def format_date_filter(value, fmt='long', lang='fr_FR'):
    """
    Formate une date en utilisant Babel.
    Convertit en datetime pour la compatibilité avec Babel mais n'affiche que la date.
    """
    if isinstance(value, str):
        # Convertir en date uniquement
        dt = datetime.strptime(value, '%Y-%m-%d').date()
    elif isinstance(value, datetime):
        dt = value.date()  # Extraire uniquement la partie date
    elif isinstance(value, date):
        dt = value
    else:
        raise ValueError(f"Type de date non reconnu: {type(value)}")

    patterns = {
        'full': 'EEEE d MMMM y',
        'long': 'd MMMM y',
        'medium': 'd MMM y',
        'short': 'dd/MM/y'
    }

    return format_date(dt, format=patterns.get(fmt, 'long'), locale=lang)


def slugify(value):
    """
    Convertit une chaîne en un slug URL-friendly.
    Exemple : "mot-clé1" → "mot-cle1"
    """
    value = str(value).strip().lower()

    value = unidecode(value)
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[-\s]+', '-', value).strip('-')

    return value
