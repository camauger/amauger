import math
import logging
from pathlib import Path
from utils import build_page
from frontmatter_parser import parse_frontmatter


class PostBuilder:
    def __init__(self, src_path: Path, dist_path: Path, site_config: dict,
                 translations: dict, jinja_env, projects):
        self.src_path = src_path
        self.dist_path = dist_path
        self.site_config = site_config
        self.translations = translations
        self.jinja_env = jinja_env
        self.projects = projects
        self.blog_url = self.site_config.get('blog_url', '/blog/').strip('/')
        self.posts_per_page = self.site_config.get('posts_per_page', 5)
        self.post_template = self.site_config.get(
            'post_template', 'posts/post.html')
        self.blog_template = self.site_config.get(
            'blog_template', 'pages/blog.html')
        self.home_template = self.site_config.get(
            'home_template', 'pages/home.html')
        self.unilingual = len(self.site_config.get('languages', [])) == 1

    def _get_posts_dir(self, lang: str) -> Path:
        """Retourne le dossier contenant les posts pour la langue donnée."""
        posts_dir = self.src_path / 'locales' / lang / 'blog'
        if not posts_dir.exists():
            posts_dir = self.src_path / 'locales' / lang / 'posts'
        return posts_dir if posts_dir.exists() else None

    def load_posts(self, lang: str) -> list:
        posts = []
        posts_dir = self._get_posts_dir(lang)
        if posts_dir:
            for post_file in posts_dir.glob('*.md'):
                content = post_file.read_text(encoding='utf-8')
                metadata, _ = parse_frontmatter(content)
                tid = str(metadata.get("translation_id",
                          metadata.get("slug", post_file.stem)))
                post_data = {
                    'title': metadata.get('title', 'Article sans titre'),
                    'date': metadata.get('date', ''),
                    'author': metadata.get('author', ''),
                    'url': (f"/{self.blog_url}/{metadata.get('slug', post_file.stem)}/"
                            if self.unilingual
                            else f"/{lang}/{self.blog_url}/{metadata.get('slug', post_file.stem)}/"),
                    'slug': metadata.get("slug", post_file.stem),
                    'translation_id': tid,
                    'summary': metadata.get('summary', ''),
                    'categories': metadata.get('categories', []),
                    'meta_keywords': metadata.get('meta_keywords', []),
                    'thumbnail': metadata.get('thumbnail', ''),
                    'lang': lang
                }
                posts.append(post_data)
        posts.sort(key=lambda x: x['date'], reverse=True)
        return posts

    def paginate_posts(self, posts: list, lang: str) -> list:
        total_pages = math.ceil(len(posts) / self.posts_per_page)
        paginated = []
        for i in range(total_pages):
            page_posts = posts[i *
                               self.posts_per_page: (i + 1) * self.posts_per_page]
            paginated.append({
                'posts': page_posts,
                'current_page': i + 1,
                'prev_page': None if i == 0 else f"/{lang}/{self.blog_url}/page/{i + 1}",
                'next_page': None if i == total_pages - 1 else f"/{lang}/{self.blog_url}/page/{i + 2}",
                'pages': [{'number': j + 1, 'url': f"/{lang}/{self.blog_url}/page/{j + 1}"} for j in range(total_pages)]
            })
        logging.info(
            f"📢 Pagination créée pour {lang}: {total_pages} pages, {len(posts)} articles")
        return paginated

    def build_translation_map(self, all_posts: list) -> dict:
        translation_map = {}
        for post in all_posts:
            tid = str(post.get("translation_id", post.get("slug")))
            translation_map.setdefault(tid, {})[post["lang"]] = post["url"]
        return translation_map

    def _build_individual_post(self, post_file: Path, lang: str, translation_map: dict) -> None:
        content = post_file.read_text(encoding='utf-8')
        metadata, _ = parse_frontmatter(content)
        slug = metadata.get("slug", post_file.stem)
        tid = str(metadata.get("translation_id", slug))
        content_translations = translation_map.get(tid, {})
        output = build_page(
            content,
            self.post_template,
            lang,
            custom_url=None,
            is_post=True,
            slug=slug,
            translations=self.translations[lang],
            site_config=self.site_config,
            projects=self.projects,
            jinja_env=self.jinja_env,
            content_translations=content_translations
        )
        output_path = (self.dist_path / self.blog_url / slug / 'index.html'
                       if self.unilingual
                       else self.dist_path / lang / self.blog_url / slug / 'index.html')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')

    def _build_paginated_pages(self, posts: list, lang: str) -> None:
        paginated = self.paginate_posts(posts, lang)
        for page in paginated:
            page_metadata = {
                'title': self.translations[lang].get('blog_title', 'Blog'),
                'description': self.translations[lang].get('blog_description', ''),
                'lang': lang,
                'url': (f"/{self.blog_url}/" if self.unilingual else f"/{lang}/{self.blog_url}/"),
                'pagination': page
            }
            logging.info(
                f"📢 Génération de la page {page['current_page']} avec {len(page['posts'])} articles")
            output = self.jinja_env.get_template(self.blog_template).render(
                pagination=page,
                page=page_metadata,
                t=self.translations[lang],
                site=self.site_config,
                projects=self.projects
            )
            if page['current_page'] == 1:
                output_path = (self.dist_path / 'blog' / 'index.html'
                               if self.unilingual
                               else self.dist_path / lang / 'blog' / 'index.html')
            else:
                output_path = (self.dist_path / 'blog' / 'page' / str(page['current_page']) / 'index.html'
                               if self.unilingual
                               else self.dist_path / lang / 'blog' / 'page' / str(page['current_page']) / 'index.html')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')

    def get_recent_posts(self, posts: list, count: int = 3) -> list:
        """Retourne les posts récents (par défaut, les 3 premiers)."""
        return posts[:count]

    def _build_home_page(self, recent_posts: list, lang: str) -> None:
        page_metadata = {
            'title': self.translations[lang].get('home_title', 'Accueil'),
            'description': self.translations[lang].get('home_description', ''),
            'lang': lang,
            'home_cta': self.translations[lang].get('home_cta', 'En savoir plus'),
            'home_image': self.translations[lang].get('home_image', ''),
        }
        output = self.jinja_env.get_template(self.home_template).render(
            page=page_metadata,
            recent_posts=recent_posts,
            t=self.translations[lang],
            site=self.site_config,
            projects=self.projects
        )
        output_path = (self.dist_path / 'index.html'
                       if self.unilingual
                       else self.dist_path / lang / 'index.html')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding='utf-8')

    def build_posts(self) -> list:
        all_posts = []
        posts_by_lang = {}
        # Charger les posts pour chaque langue
        for lang in self.site_config['languages']:
            posts_dir = self._get_posts_dir(lang)
            if posts_dir:
                posts = self.load_posts(lang)
                posts_by_lang[lang] = posts
                all_posts.extend(posts)

        # Construire le mapping global des traductions
        translation_map = self.build_translation_map(all_posts)

        # Générer les pages individuelles, paginées et la page d'accueil
        for lang, posts in posts_by_lang.items():
            posts_dir = self._get_posts_dir(lang)
            if posts_dir:
                for post_file in posts_dir.glob('*.md'):
                    self._build_individual_post(
                        post_file, lang, translation_map)
                self._build_paginated_pages(posts, lang)
                # Utiliser la méthode get_recent_posts pour obtenir les articles récents
                recent_posts = self.get_recent_posts(posts)
                self._build_home_page(recent_posts, lang)

        # Injection du mapping dans chaque post (pour usage ultérieur, log, etc.)
        for post in all_posts:
            post['translations'] = translation_map.get(
                post['translation_id'], {})
            logging.info(
                f"Post {post['slug']} translations: {post['translations']}")
        return all_posts
