Christian Amauger – Site Dev Setup
==================================

Prerequisites
-------------
- Node.js 18+ (ships with npm)
- Python 3.10+ (needed for `scripts/build.py`)
- Optional: a Python virtual environment

Initial Setup
-------------
1. Install JavaScript dependencies:
   ```
   npm install
   ```
2. (Recommended) install the Python tooling that the static site generator uses:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows PowerShell
   pip install -r requirements.txt
   ```

Running the Dev Server
----------------------
```
npm run dev
```
This runs `grunt dev`, which:
- Builds the HTML via `python scripts/build.py --build`
- Compiles Sass with source maps
- Copies static assets
- Starts a local server at <http://localhost:3000> with LiveReload
- Watches `src/`, `content/`, and `templates/` for changes

Stop the server with `Ctrl+C`. Restart if you modify `scripts/` or the Grunt config.

Production Build
----------------
Generate a minified build without starting the dev server:
```
npm run build
```
Outputs live-ready assets in the `dist/` folder (cleaned before each build).

