import os
import shutil
import errno
import stat


class StaticFileManager:
    def __init__(self, src_path, dist_path):
        self.src_path = src_path
        self.dist_path = dist_path

    def handle_remove_readonly(self, func, path, exc_info):
        exc_value = exc_info[1]
        if func in (os.rmdir, os.remove, os.unlink) and exc_value.errno == errno.EACCES:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise

    def setup_output_dir(self):
        if self.dist_path.exists():
            shutil.rmtree(self.dist_path, onerror=self.handle_remove_readonly)
        self.dist_path.mkdir(parents=True)

    def copy_static_files(self):
        static_dirs = ['styles', 'scripts', 'assets']
        for dir_name in static_dirs:
            src = self.src_path / dir_name
            if src.exists():
                dst = self.dist_path / dir_name
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
