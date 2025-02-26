---
layout: post
title: Idoine - A Purposefully Simple Static Site Generator
date: 2025-02-26
slug: idoine
categories: [transformation numerique, strategie digitale, entrepreneuriat]
summary: In a landscape where web frameworks continuously expand in complexity, _Idoine_ (pronounced "ee-dwahn") takes an intentionally different approach. This minimalist static site generator embodies a "just enough" philosophy - providing exactly what you need to create functional, lightweight, and multilingual websites without unnecessary complexity.
---

In a landscape where web frameworks continuously expand in complexity, _Idoine_ (pronounced "ee-dwahn") takes an intentionally different approach. This minimalist static site generator embodies a "just enough" philosophy - providing exactly what you need to create functional, lightweight, and multilingual websites without unnecessary complexity.

## The Story Behind the Name

The name _Idoine_ comes from French, meaning "suitable," "appropriate," or "fit for purpose." This perfectly captures the project's philosophy: providing tools that are just right for the task at hand - no more, no less. In a world of feature-rich frameworks, Idoine chooses simplicity by design.

## A Deliberate Choice of Tools

Instead of reinventing the wheel, Idoine builds upon proven, stable technologies:

- **Grunt**: For task automation and development workflow
- **Python** with Jinja2: For templating and content generation
- **SCSS**: For maintainable styling
- **Markdown**: For content writing
- **YAML**: Front matter for metadata
  This carefully curated stack prioritizes simplicity and reliability over cutting-edge features.

## Core Features

While intentionally minimal, Idoine includes essential capabilities for modern static sites:

- **Multilingual Support**: Built-in internationalization using a simple directory structure
- **Live Reload**: Development server with hot reloading for rapid iteration
- **Asset Pipeline**: Automated processing of styles, scripts, and media files
- **Production-Ready**: Optimized builds with CSS minification and proper asset handling
- **Zero Configuration**: Works out of the box with sensible defaults
- **Netlify Ready**: Seamless deployment with included Netlify configuration

## Under the Hood: The Build Pipeline

Idoine's build process is transparent and efficient, orchestrated by Grunt with Python handling the content generation:

### Development Workflow

When you run `npm run dev`, Idoine:

1. Builds all HTML pages from Markdown content using Python and Jinja2
2. Compiles SCSS to CSS with source maps for debugging
3. Applies Autoprefixer to ensure cross-browser compatibility
4. Copies static assets to the distribution folder
5. Starts a local server with live reload at `http://localhost:9000`
6. Watches for changes to rebuild only what's necessary

```javascript
// From Gruntfile.js
grunt.registerTask("dev", [
  "shell:build_html", // Run Python build script
  "convertMarkdown", // Process Markdown
  "sass:dev", // Compile SCSS with source maps
  "postcss:dev", // Apply Autoprefixer
  "copy", // Copy static assets
  "connect", // Start dev server
  "watch", // Watch for changes
]);
```

### Production Build

For production (`npm run build`), Idoine optimizes everything:

1. Cleans the distribution directory for a fresh build
2. Processes all Markdown and templates through Python
3. Compiles SCSS with optimized settings
4. Applies Autoprefixer for cross-browser support
5. Minifies CSS to reduce file size
6. Copies and optimizes static assets
   The Python build script handles the conversion from Markdown to HTML, applying templates and maintaining the multilingual structure. It processes front matter metadata, supporting custom page attributes and localized content.

## Getting Started

Idoine is designed to get you up and running quickly with minimal friction. Here's a step-by-step guide to launch your first Idoine site:

### Prerequisites

Make sure you have the following installed:

- Node.js 18 or higher
- Python 3.9 or higher
- npm (comes with Node.js)
- Git

### Initial Setup

```bash
# Clone the template repository
git clone [URL_TO_REPO]
cd idoine
# Install Node.js dependencies
npm install
# Optional but recommended: Create a Python virtual environment
python -m venv venv
source venv/bin/activate # On Unix/MacOS
# or
venv\Scripts\activate # On Windows
# Install Python dependencies
pip install -r requirements.txt
```

### Creating Your First Content

1. Navigate to the content directory for your language:
    `bash
 cd src/locales/en/pages/ # For English content
 `
2. Create a new Markdown file (e.g., `about.md`):
    ```markdown
    - -
    title: About This Site
    description: Learn more about this project
    layout: page
    - -

# About

This is a simple site created with Idoine, a minimalist static site generator.

## Features

- Fast and lightweight
 - Multilingual support
 - Easy to customize
 `
3. Start the development server:
 `bash
 npm run dev
 ```4. Visit`http://localhost:9000/about` to see your new page.

### Adding a New Language

Idoine makes multilingual content straightforward:

1. Create a new language directory:
    `bash
 mkdir -p src/locales/es/pages
 `
2. Add content in the new language:
    `bash
 touch src/locales/es/pages/index.md
 `
3. Edit the file with localized content.
4. Restart the development server, and your site will now support the new language.

### Customizing Templates

To modify the site's appearance:

1. Edit templates in the `templates/` directory to adjust layouts
2. Modify SCSS files in `src/styles/` to change the styling
3. Add custom fonts or images to `src/assets/`
   The development server will automatically reload when you save changes, giving you immediate feedback.

## A Template to Build Upon

While Idoine is minimal, it's also designed to be extended. The project structure is clear and logical:

```
/
├── dist/ # Generated site output
├── src/
│ ├── assets/ # Static files
│ │ ├── fonts/ # Web fonts
│ │ └── images/ # Image assets
│ ├── locales/ # Multilingual content
│ │ ├── fr/ # French content
│ │ │ └── pages/ 
│ │ └── en/ # English content
│ │ └── pages/
│ └── styles/ # SCSS files
├── scripts/ # Python build scripts
├── templates/ # Jinja2 templates
├── Gruntfile.js # Grunt configuration
└── requirements.txt # Python dependencies
```

The separation between content (`/src/locales`), presentation (`/templates`), and styling (`/src/styles`) makes it easy to maintain and extend your site as it grows. Content is written in Markdown with YAML front matter:

```markdown
- -
title: Welcome to My Site
description: A simple homepage built with Idoine
layout: home
 - -

# Welcome

This is the homepage content written in **Markdown**.
```

Templates use Jinja2 for powerful and flexible layouts:

```html
{% extends "base.html" %} {% block content %}  
<main class="home"> {{ content | safe }}  </main>
{% endblock %}
```

## Join the Simplicity Movement

Idoine doesn't aim to compete with feature-rich static site generators. Instead, it offers a starting point for those who value:

- Simplicity over complexity
- Convention over configuration
- Focus over feature-bloat
- Stability over bleeding-edge features
  If this philosophy resonates with you, give Idoine a try. Clone the template, create your content, and enjoy a straightforward path to a multilingual static site.
  Remember: sometimes, less is more. And that's exactly what Idoine strives to be - *idoine* for your needs.
