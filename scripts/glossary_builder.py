import math
from utils import build_page, slugify
import logging


class GlossaryBuilder:
    def __init__(self, src_path, dist_path, site_config, translations, jinja_env, projects):
        self.src_path = src_path
        self.dist_path = dist_path
        self.site_config = site_config
        self.translations = translations
        self.jinja_env = jinja_env
        self.projects = projects
        self.glossary_url = self.site_config.get(
            'glossary_url', '/glossaire/').strip('/')
        self.terms_per_page = self.site_config.get('terms_per_page', 10)
        self.term_template = self.site_config.get(
            'term_template', 'pages/glossary-term.html')
        self.glossary_template = self.site_config.get(
            'glossary_template', 'pages/glossary.html')
        self.unilingual = len(self.site_config.get('languages', [])) == 1

    def _parse_frontmatter(self, content):
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                _, frontmatter, markdown_content = parts
                metadata = {}
                for line in frontmatter.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()

                        if key in ['categories', 'meta_keywords', 'tags']:
                            if value.startswith('[') and value.endswith(']'):
                                try:
                                    value = [v.strip()
                                             for v in value.strip('[]').split(',')]
                                except:
                                    value = []
                            else:
                                value = [v.strip()
                                         for v in value.split(',') if v.strip()]

                        metadata[key] = value
                return metadata, markdown_content
        return {}, content

    def load_terms(self, lang):
        terms = []
        terms_dir = self.src_path / 'locales' / lang / 'glossaire'
        if terms_dir.exists():
            for term_file in terms_dir.glob('*.md'):
                content = term_file.read_text(encoding='utf-8')
                metadata, _ = self._parse_frontmatter(content)
                slug = metadata.get("slug", term_file.stem)
                term_data = {
                    'title': metadata.get('title', 'Terme sans titre'),
                    'date': metadata.get('date', ''),
                    'author': metadata.get('author', ''),
                    'url': f"/{self.glossary_url}/{slug}/" if self.unilingual else f"/{lang}/{self.glossary_url}/{slug}/",
                    'slug': slug,
                    'summary': metadata.get('summary', ''),
                    'categories': metadata.get('categories', []),
                    'meta_keywords': metadata.  get('meta_keywords', []),
                    'tags': metadata.get('tags', []),

                    'thumbnail': metadata.get('thumbnail', ''),
                    'lang': lang
                }
                terms.append(term_data)
        terms.sort(key=lambda x: x['title'])
        return terms

    def paginate_terms(self, terms, lang):
        total_pages = math.ceil(len(terms) / self.terms_per_page)
        prefix = "" if self.unilingual else f"/{lang}"
        paginated = []
        for i in range(total_pages):
            page_terms = terms[i *
                               self.terms_per_page: (i + 1) * self.terms_per_page]
            paginated.append({
                'terms': page_terms,
                'current_page': i + 1,
                'prev_page': None if i == 0 else f"{prefix}/{self.glossary_url}/page/{i}",
                'next_page': None if i == total_pages - 1 else f"{prefix}/{self.glossary_url}/page/{i + 2}",
                'pages': [{'number': j + 1, 'url': f"{prefix}/{self.glossary_url}/page/{j + 1}"} for j in range(total_pages)]
            })
        return paginated

    def _build_individual_term(self, term_file, lang):
        content = term_file.read_text(encoding='utf-8')
        metadata, _ = self._parse_frontmatter(content)
        slug = metadata.get("slug", term_file.stem)
        output = build_page(
            content,
            self.term_template,
            lang,
            custom_url=None,
            is_post=True,
            slug=slug,
            translations=self.translations[lang],
            site_config=self.site_config,
            projects=self.projects,
            jinja_env=self.jinja_env
        )
        if self.unilingual:
            output_path = self.dist_path / self.glossary_url / slug / 'index.html'
        else:
            output_path = self.dist_path / lang / self.glossary_url / slug / 'index.html'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')

    def _build_paginated_pages(self, terms, lang):
        paginated = self.paginate_terms(terms, lang)
        for page in paginated:
            page_metadata = {
                'title': self.translations[lang].get('glossary_title', 'Glossaire'),
                'description': self.translations[lang].get('glossary_description', ''),
                'lang': lang,
                'url': f"/{self.glossary_url}/" if self.unilingual else f"/{lang}/{self.glossary_url}/"
            }
            output = self.jinja_env.get_template(self.glossary_template).render(
                pagination=page,
                page=page_metadata,
                t=self.translations[lang],
                site=self.site_config,
                projects=self.projects
            )
            if page['current_page'] == 1:
                if self.unilingual:
                    output_path = self.dist_path / self.glossary_url / 'index.html'
                else:
                    output_path = self.dist_path / lang / self.glossary_url / 'index.html'
            else:
                if self.unilingual:
                    output_path = self.dist_path / self.glossary_url / \
                        'page' / str(page['current_page']) / 'index.html'
                else:
                    output_path = self.dist_path / lang / self.glossary_url / \
                        'page' / str(page['current_page']) / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')

    def build_tag_pages(self, terms_by_lang):
        tag_dict = {}

        for lang, terms in terms_by_lang.items():
            for term in terms:
                tags = term.get('tags', [])
                if not isinstance(tags, list):
                    logging.warning(
                        f"❌ Tags incorrects pour {term['title']}: {tags}")
                    continue

                for tag in tags:
                    tag_slug = slugify(tag)
                    tag_dict.setdefault(tag_slug, {}).setdefault(
                        lang, []).append(term)

        for tag_slug, terms_by_language in tag_dict.items():
            for lang, terms in terms_by_language.items():
                logging.info(f"🔖 Génération de la page du tag: {tag_slug}")

                tag_metadata = {
                    'title': f"Tag: {tag_slug.replace('-', ' ')}",
                    'description': f"Tous les termes liés à {tag_slug}",
                    'lang': lang,
                    'url': f"/{self.glossary_url}/tags/{tag_slug}/"
                }

                output = self.jinja_env.get_template('pages/glossary-tag.html').render(
                    terms=terms,
                    page=tag_metadata,
                    t=self.translations[lang],
                    site=self.site_config,
                    projects=self.projects
                )

                if self.unilingual:
                    output_path = self.dist_path / self.glossary_url / 'tags' / tag_slug / 'index.html'
                else:
                    output_path = self.dist_path / lang / \
                        self.glossary_url / 'tags' / tag_slug / 'index.html'

                logging.info(f"📄 Page du tag générée : {output_path}")

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(output, encoding='utf-8')

    def build_terms(self):
        all_terms = []
        terms_by_lang = {}
        for lang in self.site_config['languages']:
            terms_dir = self.src_path / 'locales' / lang / 'glossaire'
            if terms_dir.exists():
                terms = self.load_terms(lang)
                terms_by_lang[lang] = terms
                all_terms.extend(terms)
        for lang, terms in terms_by_lang.items():
            terms_dir = self.src_path / 'locales' / lang / 'glossaire'
            for term_file in terms_dir.glob('*.md'):
                self._build_individual_term(term_file, lang)
            self._build_paginated_pages(terms, lang)

        self.build_tag_pages(terms_by_lang)

        return all_terms
