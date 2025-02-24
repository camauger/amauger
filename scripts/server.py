import http.server
import socketserver
from urllib.parse import unquote
import os

PORT = 9000
DIRECTORY = "dist"


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = unquote(path)
        path = path.lstrip('/')
        full_path = os.path.join(DIRECTORY, path)

        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                return os.path.join(full_path, 'index.html')
            return full_path

        if not os.path.splitext(full_path)[1]:
            full_path_html = full_path + '.html'
            if os.path.exists(full_path_html):
                return full_path_html

        return full_path


Handler = CustomHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
