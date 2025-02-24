# IDOINE

Générateur de site/blog modulable avec support multilingue basé sur Grunt et Python.

[![Node Version](https://img.shields.io/badge/node-18%2B-brightgreen.svg)]()
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

## 📋 Table des matières

1. [Prérequis](#-prérequis)
2. [Installation](#-installation)
3. [Utilisation](#-utilisation)
4. [Structure du projet](#-structure-du-projet)
5. [Pipeline de build](#-pipeline-de-build)
6. [Configuration](#-configuration)
7. [Déploiement](#-déploiement)
8. [Contribution](#-contribution)

## 🔧 Prérequis

- Node.js 18 ou supérieur
- Python 3.9 ou supérieur
- npm
- grunt-cli installé globalement (`npm install -g grunt-cli`)

## 💻 Installation

1. Cloner le dépôt :

```bash
git clone [URL_DU_REPO]
cd idoine
```

2. Installer les dépendances Node.js :

```bash
npm install
```

3. Créer et activer un environnement virtuel Python :

```bash
python -m venv venv
source venv/bin/activate  # Sur Unix
venv\Scripts\activate     # Sur Windows
```

4. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Développement

Lance un serveur de développement avec rechargement à chaud :

```bash
npm run dev
```

Le site sera accessible sur `http://localhost:9000`

### Production

Génère une version optimisée du site :

```bash
npm run build
```

## 📁 Structure du projet

```
/
├── dist/                # Fichiers générés
├── src/
│   ├── assets/         # Images, polices...
│   │   ├── fonts/
│   │   └── images/
│   ├── locales/        # Contenu multilingue
│   │   ├── fr/
│   │   └── en/
│   └── styles/         # Fichiers SCSS
├── scripts/            # Scripts Python
├── templates/          # Templates du site
├── Gruntfile.js       # Configuration Grunt
├── netlify.toml       # Configuration Netlify
├── package.json       # Dépendances Node.js
└── requirements.txt    # Dépendances Python
```

## 🔄 Pipeline de build

Le processus de build, géré par Grunt, comprend :

1. Nettoyage du dossier `dist`
2. Compilation SCSS vers CSS
3. Post-processing CSS (Autoprefixer)
4. Minification CSS pour la production
5. Conversion Markdown en HTML
6. Copie des assets statiques
7. Construction des pages via Python

## ⚙️ Configuration

### Grunt

Le fichier `Gruntfile.js` définit les tâches principales :

- `grunt dev` : Environnement de développement
- `grunt build` : Build de production
- `grunt sass` : Compilation SCSS
- `grunt watch` : Surveillance des fichiers

### Python

Les scripts Python gèrent :

- La conversion Markdown vers HTML
- Le routage multilingue
- La génération des pages

## 🌐 Déploiement

Le projet est configuré pour Netlify :

```toml
[build]
  command = """
    npm install -g grunt-cli sass &&
    npm install &&
    pip install -r requirements.txt &&
    grunt build
  """
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"
  PYTHON_VERSION = "3.9"
```

## 👥 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Créer une Pull Request

### Guide de style

- Respecter le style des fichiers existants
- Documenter les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire
