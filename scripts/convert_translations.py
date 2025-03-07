import yaml
import json
import os
from pathlib import Path
import re
import argparse

def convert_to_icu_format(key, value):
    """Convert standard translation strings to ICU MessageFormat where applicable"""

    # Handle reading time with minutes
    if key == 'reading_time':
        return "{minutes, plural, =0{Less than a minute} =1{1 minute} other{# minutes}} read"

    # Handle post counts
    if 'count' in key.lower() or key in ['no_article']:
        return "{count, plural, =0{No articles} one{# article} other{# articles}}"

    # Handle date formatting
    if key in ['published_on', 'published_date', 'updated_on', 'updated_date']:
        if 'published' in key:
            return "Published on {date, date, medium}"
        else:
            return "Updated on {date, date, medium}"

    # Handle comments
    if key == 'comments':
        return "{count, plural, =0{No comments} one{# comment} other{# comments}}"

    return value

def organize_by_namespace(translations):
    """Organize translations into logical namespaces"""
    namespaces = {
        'common': {},
        'blog': {},
        'gallery': {},
        'glossary': {},
        'home': {},
        'pagination': {},
        'forms': {}
    }

    # Define namespace mappings
    namespace_map = {
        # Common namespace
        'about': 'common',
        'all_rights_reserved': 'common',
        'close': 'common',
        'dark_mode': 'common',
        'light_mode': 'common',
        'language': 'common',
        'menu': 'common',
        'nav_label': 'common',
        'search': 'common',
        'search_placeholder': 'common',
        'skip_to_content': 'common',
        'social_links': 'common',

        # Blog namespace
        'blog': 'blog',
        'categories': 'blog',
        'keywords': 'blog',
        'tags': 'blog',
        'latest_posts': 'blog',
        'read_more': 'blog',
        'reading_time': 'blog',
        'recent_posts': 'blog',
        'related_posts': 'blog',
        'view_all_posts': 'blog',
        'written_by': 'blog',
        'published_on': 'blog',
        'updated_on': 'blog',
        'no_article': 'blog',
        'post_header': 'blog',
        'post_footer': 'blog',
        'post_featured': 'blog',
        'draft': 'blog',

        # Gallery namespace
        'gallery_title': 'gallery',
        'image_preview': 'gallery',
        'image_page': 'gallery',
        'image_download': 'gallery',
        'no_image_found': 'gallery',
        'download_small': 'gallery',
        'download_medium': 'gallery',
        'download_large': 'gallery',
        'download_original': 'gallery',
        'size_small': 'gallery',
        'size_medium': 'gallery',
        'size_large': 'gallery',
        'size_original': 'gallery',
        'back_to_gallery': 'gallery',
        'image_page_title': 'gallery',
        'image_meta_description': 'gallery',
        'image_gallery_title': 'gallery',
        'number_of_images': 'gallery',

        # Home namespace
        'home': 'home',
        'home_title': 'home',
        'portfolio_button': 'home',
        'portfolio_subtitle': 'home',
        'portfolio_title': 'home',
        'learn_more': 'home',
        'project_title_default': 'home',
        'project_description_default': 'home',
        'hero_cta': 'home',

        # Pagination namespace
        'next': 'pagination',
        'previous': 'pagination',
        'next_page': 'pagination',
        'previous_page': 'pagination',
        'go_to_page': 'pagination',

        # Glossary namespace
        'glossary_title': 'glossary',
        'glossary_description': 'glossary',
        'glossary_thumbnail_alt': 'glossary',

        # Development section
        'developpement_web': 'home',
        'developpement_web_description': 'home',
        'jeux_de_role': 'home',
        'jeux_de_role_description': 'home',
        'strategie_numerique': 'home',
        'strategie_numerique_description': 'home'
    }

    # Fallback namespace is 'common'
    for key, value in translations.items():
        namespace = namespace_map.get(key, 'common')
        namespaces[namespace][key] = convert_to_icu_format(key, value)

    # Remove empty namespaces
    return {k: v for k, v in namespaces.items() if v}

def convert_yaml_to_json_files(yaml_path, output_dir):
    """Convert YAML translations to JSON files organized by namespace"""
    # Load YAML file
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    # Process each language
    for lang, translations in yaml_data.items():
        lang_dir = Path(output_dir) / lang
        lang_dir.mkdir(parents=True, exist_ok=True)

        # Organize translations by namespace
        namespaces = organize_by_namespace(translations)

        # Write each namespace to a separate JSON file
        for namespace, content in namespaces.items():
            output_file = lang_dir / f"{namespace}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"Created {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YAML translations to JSON files with ICU MessageFormat")
    parser.add_argument("yaml_file", help="Path to the YAML translations file")
    parser.add_argument("--output-dir", "-o", default="src/data/translations.yaml", help="Output directory for JSON files")

    args = parser.parse_args()
    convert_yaml_to_json_files(args.yaml_file, args.output_dir)
    print("Conversion completed successfully!")
