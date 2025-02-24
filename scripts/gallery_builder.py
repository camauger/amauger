import os
import logging
from pathlib import Path
from jinja2 import Environment
from gallery_utils import find_images_dir, find_image_files, copy_images


class GalleryBuilder:
    def __init__(self, src_path: Path, dist_path: Path, jinja_env: Environment, site_config: dict, translations: dict):
        self.src_path = src_path
        self.dist_path = dist_path
        self.jinja_env = jinja_env
        self.site_config = site_config
        self.translations = translations
        self.gallery_template = self.site_config.get(
            'gallery_template', 'pages/gallery.html')
        self.languages = self.site_config.get(
            'languages') or [self.site_config.get('lang', 'fr')]
        self.unilingual = len(self.languages) == 1

    def build_gallery(self):
        candidate = self.src_path / "assets/gallery_images"
        if candidate.exists():
            images_dir = candidate
        else:
            images_dir = find_images_dir(self.src_path)

        copy_images(images_dir, self.dist_path)

        images = find_image_files(images_dir)

        if self.unilingual:
            lang = self.languages[0]
            gallery_url = "/gallery/"            # URL pour la page de détail de l'image
            prefix = "/assets/gallery_images/"    # Préfixe pour accéder aux images copiées
            output_gallery_dir = self.dist_path / "gallery"
            output_gallery_dir.mkdir(parents=True, exist_ok=True)
            context = {
                'gallery': images,
                'lang': lang,
                'prefix': prefix,
                'url': gallery_url,
                't': self.translations.get(lang, {}),
                'site': self.site_config,
                'page': {
                    'lang': lang,
                    'url': gallery_url,
                    'title': self.translations.get(lang, {}).get('gallery_title', 'Gallery'),
                }
            }
            rendered = self.jinja_env.get_template(
                self.gallery_template).render(**context)
            output_index = output_gallery_dir / "index.html"
            output_index.parent.mkdir(parents=True, exist_ok=True)
            output_index.write_text(rendered, encoding="utf-8")
            self._render_image_pages(
                output_gallery_dir, images_dir, images, prefix, context['page'])
        else:
            for lang in self.languages:
                gallery_url = f"/{lang}/gallery/"
                prefix = "/assets/gallery_images/"
                output_gallery_dir = self.dist_path / lang / "gallery"
                output_gallery_dir.mkdir(parents=True, exist_ok=True)
                context = {
                    'gallery': images,
                    'lang': lang,
                    'prefix': prefix,
                    'url': gallery_url,
                    't': self.translations.get(lang, {}),
                    'site': self.site_config,
                    'page': {
                        'lang': lang,
                        'url': gallery_url,
                        'title': self.translations.get(lang, {}).get('gallery_title', 'Gallery'),
                    }
                }
                rendered = self.jinja_env.get_template(
                    self.gallery_template).render(**context)
                output_index = output_gallery_dir / "index.html"
                output_index.parent.mkdir(parents=True, exist_ok=True)
                output_index.write_text(rendered, encoding="utf-8")
                self._render_image_pages(
                    output_gallery_dir, images_dir, images, prefix, context['page'])

    def _get_gallery_output(self):
        """
        Retourne le répertoire de sortie, le préfixe pour les URLs et les informations de page
        en fonction de la configuration multilingue.
        """
        if self.site_config.get("multilang", False):
            lang = self.site_config.get("lang", "fr")
            lang_dir = self.dist_path / lang
            lang_dir.mkdir(parents=True, exist_ok=True)
            output_gallery_dir = lang_dir / "gallery"
            prefix = "../../"
            page_info = {"lang": lang}
        else:
            output_gallery_dir = self.dist_path / "gallery"
            prefix = "../"
            page_info = {}
        output_gallery_dir.mkdir(parents=True, exist_ok=True)
        return output_gallery_dir, prefix, page_info

    def _render_gallery_page(self, output_gallery_dir, gallery_files, prefix, page_info):
        """
        Rendu de la page principale de la galerie.
        """
        logging.info(
            "Final gallery_files passed to template: %s", gallery_files)
        template = self.jinja_env.get_template('pages/gallery.html')
        logging.info("Template path: %s", template.filename)
        gallery_html = template.render(
            gallery=gallery_files,
            prefix=prefix,
            page=page_info,
            site=self.site_config,
            t=self.translations.get(page_info['lang'], {})
        )
        output_file = output_gallery_dir / "index.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(gallery_html)

    def _render_image_pages(self, output_gallery_dir, images_dir, image_files, prefix, page_info):
        """
        Génère une page HTML pour chaque image.
        """
        template = self.jinja_env.get_template('pages/image.html')
        for image in image_files:
            image_stem = os.path.splitext(image)[0]
            logging.info("Création de la page pour l'image: %s", image)
            image_url = f"{prefix}{image}"
            image_versions = {
                'small': f"{prefix}small/{image}",
                'medium': f"{prefix}medium/{image}",
                'large': f"{prefix}large/{image}",
                'original': image_url
            }
            image_html = template.render(
                image=image_url,
                image_name=image_stem,
                image_versions=image_versions,
                page=page_info,
                site=self.site_config,
                t=self.translations.get(page_info['lang'], {}),
                prefix=prefix
            )
            output_file = output_gallery_dir / f"{image_stem}.html"
            logging.info("Écriture de la page dans : %s", output_file)
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(image_html)
            except Exception as e:
                logging.error(
                    "Erreur lors de l'écriture de %s: %s", output_file, e)


if __name__ == '__main__':
    from jinja2 import Environment, FileSystemLoader
    from pathlib import Path
    logging.basicConfig(level=logging.INFO)
    jinja_env = Environment(loader=FileSystemLoader('src/templates'))
    gallery_builder = GalleryBuilder(
        Path("src"),
        Path("dist"),
        jinja_env,
        {"lang": "fr", "multilang": True},
        {}
    )
    gallery_builder.build_gallery()
    logging.info("📸 Galerie d'images générée avec succès!")
