---
layout: post
title: Idoine - A Purposefully Simple Static Site Generator
date: 2025-03-07
slug: idoine
thumbnail: /assets/images/lego.jpg
categories: [idoine, web]
summary: In an era of increasingly complex web frameworks, Idoine stands out with intentional simplicity.
---

In an era of increasingly complex web frameworks, _Idoine_ (pronounced "ee-dwahn") stands out with intentional simplicity. This minimalist static site generator embodies a "just enough" philosophy—providing exactly what you need to create functional, lightweight, and multilingual websites without unnecessary complexity.

## The Story Behind the Name

The name [_Idoine_](https://github.com/camauger/idoine) comes from French, meaning "suitable," "appropriate," or "fit for purpose." This captures the project's philosophy: offering exactly the tools required—nothing more, nothing less. In a world dominated by feature-rich frameworks, Idoine deliberately embraces simplicity.

## A Deliberate Choice of Tools

Rather than reinventing the wheel, Idoine leverages proven, stable technologies:

- **Grunt** – Task automation and streamlined workflows
- **Python** with Jinja2 – Efficient templating and content generation
- **SCSS** – Maintainable styling
- **Markdown** – Straightforward content writing
- **YAML** – Structured metadata through front matter

This carefully curated stack prioritizes simplicity and reliability over cutting-edge complexity.

## Core Features

Idoine includes essential capabilities for modern static sites:

- **Multilingual Support** – Built-in internationalization using a clear directory structure
- **Live Reload** – Development server with instant updates for rapid iteration
- **Asset Pipeline** – Automated processing of styles, scripts, and media files
- **Production-Ready** – Optimized builds with CSS minification and efficient asset handling
- **Zero Configuration** – Immediate usability with sensible defaults
- **Netlify Ready** – Seamless deployment with built-in Netlify configuration

## Under the Hood: The Build Pipeline

Idoine's build process is transparent and efficient, orchestrated by Grunt with Python managing content generation.

### Development Workflow

When you run `npm run dev`, Idoine performs the following steps:

1. Generates HTML from Markdown using Python and Jinja2
2. Compiles SCSS to CSS with source maps for debugging
3. Applies Autoprefixer for cross-browser compatibility
4. Copies static assets to the distribution folder
5. Starts a local server with live reload at `http://localhost:9000`
6. Watches for changes, rebuilding only necessary files

```javascript
grunt.registerTask("dev", [
  "shell:build_html",
  "convertMarkdown",
  "sass:dev",
  "postcss:dev",
  "copy",
  "connect",
  "watch",
]);
```

### Production Build

The production build (`npm run build`) optimizes all assets:

1. Cleans the distribution directory for a fresh build
2. Processes all Markdown and templates through Python
3. Compiles SCSS with optimized settings
4. Applies Autoprefixer for broader browser support
5. Minifies CSS for smaller file sizes
6. Copies and optimizes static assets

The Python build script converts Markdown content to HTML, applies templates, and manages multilingual structures. It also processes YAML front matter, enabling custom attributes and localized content.

## Getting Started

Idoine helps you quickly set up your first static site with minimal effort.

### Prerequisites

Make sure you have installed:

- Node.js 18 or higher
- Python 3.9 or higher
- npm (bundled with Node.js)
- Git

### Initial Setup

```bash
git clone [https://github.com/camauger/idoine]
cd idoine
npm install
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
pip install -r requirements.txt
```

### Adding a New Language

Creating multilingual content is straightforward:

1. Create a new language directory:
   ```bash
   mkdir -p src/locales/es/pages
   ```
2. Add localized content:
   ```bash
   touch src/locales/es/pages/index.md
   ```
3. Populate the new Markdown file with content.
4. Restart the development server; your site now supports the new language.

### Customizing Templates

Modify your site's appearance easily:

- Edit layouts in the `templates/` directory.
- Update styling by editing SCSS files in `src/styles/`.
- Add fonts or images to `src/assets/`.

Live reload ensures immediate feedback as you save changes.

## A Template to Build Upon

Though minimalist, Idoine is designed for extensibility. Its clear project structure neatly separates content (`/src/locales`), templates (`/templates`), and styles (`/src/styles`), making your site easy to maintain as it evolves.

## Join the Simplicity Movement

Idoine doesn't aim to compete with more complex static site generators. Instead, it provides a straightforward alternative for developers who value:

- Simplicity over complexity
- Convention over configuration
- Focus over feature-bloat
- Stability over cutting-edge experimentation

If this resonates with you, give Idoine a try. Clone the template, create content, and experience the simplicity firsthand. Sometimes, less truly is more—exactly what makes Idoine perfectly _idoine_ for your needs.

Discover more about Idoine on [GitHub](<[_Idoine_](https://github.com/camauger/idoine)>) and start building your next project with purposeful simplicity.
