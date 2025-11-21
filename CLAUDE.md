# CLAUDE.md - AI Development Guide

This document provides guidance for working with Claude Code and AI assistants on the christianamauger.com website project.

## Project Overview

This is a personal website for Christian Amauger, built using the [Idoine template](https://github.com/camauger/idoine). The site showcases work as a Frontend Developer, Digital Strategist, and game creator.

**Tech Stack:**
- Static site generator (Python-based)
- SASS for styling
- Grunt for task automation
- Multilingual support (French/English)
- Markdown for content

## Project Structure

```
/home/user/amauger/
├── src/
│   ├── locales/
│   │   ├── fr/          # French content
│   │   │   ├── blog/    # Blog posts in French
│   │   │   ├── pages/   # Static pages
│   │   │   └── glossaire/
│   │   └── en/          # English content
│   │       ├── posts/   # Blog posts in English
│   │       └── pages/   # Static pages
│   └── assets/          # Images, CSS, JS
├── scripts/
│   └── build.py         # Python build script
├── Gruntfile.js         # Grunt task configuration
├── package.json         # Node dependencies
├── requirements.txt     # Python dependencies
└── _redirects           # Netlify redirects
```

## Development Workflow

### Setup & Installation

```bash
# Install Node dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### Common Commands

```bash
# Development mode with watch
npm run dev
# or
grunt dev

# Production build
npm run build
# or
grunt sass:prod && python scripts/build.py --build
```

### Git Workflow

The project uses feature branches with a specific naming convention:
- Branch format: `claude/<description>-<session-id>`
- Current branch: `claude/create-claude-docs-01SKATbNgK8Cm4FrdX53BAZv`
- Always push with: `git push -u origin <branch-name>`

## Working with Claude Code

### Content Creation

When creating or editing content:

1. **Blog Posts:** Add markdown files to `src/locales/{lang}/blog/` or `src/locales/{lang}/posts/`
2. **Pages:** Modify files in `src/locales/{lang}/pages/`
3. **Front Matter:** Each markdown file should include YAML front matter:
   ```yaml
   ---
   title: Page Title
   description: Page description
   template: pages/template-name.html
   ---
   ```

### Multilingual Content

Always consider both languages when making content changes:
- French: `src/locales/fr/`
- English: `src/locales/en/`

If you update content in one language, ask if the other language needs updates too.

### Style Changes

1. **SASS files:** Located in the source directories
2. **Build process:** Run `grunt sass:prod` to compile SASS to CSS
3. **Autoprefixer:** Automatically applied during build

### Testing Changes

Before committing:
1. Run `npm run dev` to test locally
2. Verify both French and English pages
3. Check responsive design on different viewports
4. Validate accessibility standards

## Best Practices for AI Assistance

### 1. Always Read Before Modifying
- Use the Read tool to examine existing files before making changes
- Understand the project structure and conventions
- Match existing code style and formatting

### 2. Preserve Existing Patterns
- Follow the established multilingual structure
- Maintain YAML front matter format
- Keep consistent markdown formatting
- Respect the Idoine template conventions

### 3. Avoid Over-Engineering
- Make minimal, focused changes
- Don't add unnecessary features or refactoring
- Keep solutions simple and maintainable
- Don't add dependencies without justification

### 4. Content Guidelines
- Match the professional, creative tone of existing content
- Use proper French accents and grammar for FR content
- Keep descriptions concise but informative
- No emojis unless explicitly requested

### 5. Version Control
- Commit related changes together
- Write clear, descriptive commit messages
- Test before pushing
- Push to the designated Claude branch only

## Common Tasks

### Adding a New Blog Post

1. Create markdown file in `src/locales/fr/blog/` or `src/locales/en/posts/`
2. Add front matter with title, description, and template
3. Write content in markdown
4. Run build to generate HTML
5. Test locally

### Updating Styles

1. Locate relevant SASS file
2. Make style changes
3. Run `grunt sass:prod`
4. Test in browser
5. Verify cross-browser compatibility

### Modifying Templates

1. Templates are handled by the Idoine framework
2. Consult Idoine documentation for template modifications
3. Test changes across all pages using that template

## Deployment

The site is deployed on Netlify:
- Redirects configured in `_redirects` file
- Configuration in `netlify.toml`
- Build command: `npm run build`

## Getting Help

### Project-Specific Issues
- Review Idoine template documentation: https://github.com/camauger/idoine
- Check existing blog posts for content examples
- Examine `Gruntfile.js` for build task details

### Claude Code Features
- Use `/help` for Claude Code assistance
- Report issues: https://github.com/anthropics/claude-code/issues

## File Naming Conventions

- **Blog posts:** Lowercase, hyphen-separated (e.g., `veille-introduction.md`)
- **Pages:** Lowercase, descriptive (e.g., `about.md`, `home.md`)
- **Keep consistent:** Match existing naming patterns

## Security & Privacy

- Never commit sensitive data (.env files, credentials)
- Review all changes before committing
- Be mindful of personal information in content

## Notes for Future Development

- Consider adding README.md with setup instructions for new developers
- Document any custom Grunt tasks added
- Keep this CLAUDE.md updated as the project evolves

---

**Last Updated:** 2025-11-21
**Template:** Idoine v1.0.0
**Maintained by:** Christian Amauger
