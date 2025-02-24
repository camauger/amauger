import logging
import shutil
from pathlib import Path


def find_images_dir(src_path: Path) -> Path:
    """
    Cherche le dossier d'images en vérifiant plusieurs emplacements.
    """
    images_dir = src_path / "assets/gallery_images"
    if not images_dir.exists():
        images_dir = src_path.parent / "assets/gallery_images"
    if not images_dir.exists():
        images_dir = src_path.parent.parent / "assets/images"
    return images_dir


def find_image_files(images_dir: Path) -> list:
    """
    Retourne la liste des fichiers images (formats PNG, JPG, JPEG, GIF)
    sous forme de chemins relatifs en notation posix.
    """
    if not images_dir.exists():
        return []
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    return [p.relative_to(images_dir).as_posix() for p in images_dir.glob('**/*')
            if p.is_file() and p.suffix.lower() in image_extensions]


def copy_images(images_dir: Path, dist_path: Path) -> None:
    """
    Copie les images depuis le dossier source vers assets/gallery_images en conservant l'arborescence.
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    target_images_dir = dist_path / "assets" / "gallery_images"
    target_images_dir.mkdir(parents=True, exist_ok=True)
    for src_image in images_dir.glob('**/*'):
        if src_image.is_file() and src_image.suffix.lower() in image_extensions:
            relative_path = src_image.relative_to(images_dir)
            dst_image = target_images_dir / relative_path
            dst_image.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_image, dst_image)
            logging.info("Copié : %s -> %s", src_image, dst_image)
