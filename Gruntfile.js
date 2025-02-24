module.exports = function (grunt) {
  // Chargement automatique de tous les plugins grunt
  require("load-grunt-tasks")(grunt);

  const fs = require("fs");
  const sass = require("sass");
  const marked = require("marked");
  const matter = require("gray-matter");

  // Tâche personnalisée pour convertir du Markdown en HTML avec gestion d'erreur
  grunt.registerTask(
    "convertMarkdown",
    "Convertit du contenu Markdown en HTML",
    function () {
      const filePath = "src/locales/fr/pages/home.md";
      try {
        const fileContent = fs.readFileSync(filePath, "utf8");
        const parsed = matter(fileContent);
        const markdownContent = parsed.content;
        const htmlContent = marked.parse(markdownContent);
        grunt.log.writeln("Contenu HTML converti :\n" + htmlContent);
      } catch (error) {
        grunt.log.error("Erreur lors de la conversion Markdown : " + error);
        return false;
      }
    }
  );

  grunt.initConfig({
    pkg: grunt.file.readJSON("package.json"),

    // Nettoyage des fichiers
    clean: {
      all: ["dist/**/*"],
      styles: ["dist/styles/**/*.{css,css.map}"],
    },

    mkdir: {
      styles: {
        options: {
          create: ["dist/styles"],
        },
      },
    },

    // Compilation Sass
    sass: {
      options: {
        implementation: sass,
      },
      // Configuration pour le développement
      dev: {
        options: {
          sourceMap: true,
          style: "expanded",
        },
        files: {
          "dist/styles/main.css": "src/styles/main.scss",
        },
      },
      // Configuration pour la production
      prod: {
        options: {
          sourceMap: false,
          style: "compressed",
        },
        files: {
          "dist/styles/main.css": "src/styles/main.scss",
        },
      },
    },
    // PostCSS avec Autoprefixer
    postcss: {
      options: {
        processors: [require("autoprefixer")()],
      },
      dev: {
        src: "dist/styles/main.css",
      },
      prod: {
        src: "dist/styles/main.css",
      },
    },

    // Minification CSS (pour la production)
    cssmin: {
      prod: {
        files: {
          "dist/styles/main.min.css": ["dist/styles/main.css"],
        },
      },
    },

    // Copie des assets (utilise grunt-newer pour ne copier que les fichiers modifiés)
    copy: {
      fonts: {
        expand: true,
        cwd: "src/assets/fonts",
        src: "**/*",
        dest: "dist/assets/fonts/",
      },
      images: {
        expand: true,
        cwd: "src/assets/images",
        src: "**/*",
        dest: "dist/assets/images/",
      },
    },

    shell: {
      build_html: {
        command: "python scripts/build.py --build",
      },
    },

    // Serveur de développement
    connect: {
      server: {
        options: {
          port: 9000,
          hostname: "localhost",
          base: "dist",
          livereload: true,
        },
      },
    },

    // Surveillance des fichiers
    watch: {
      options: {
        livereload: true,
      },
      styles: {
        files: ["src/styles/**/*.scss"],
        tasks: ["clean:styles", "sass:dev", "postcss:dev"],
      },
      assets: {
        files: "src/assets/**/*",
        tasks: ["newer:copy"],
      },
      content: {
        files: ["content/**/*", "templates/**/*"],
        tasks: ["shell:build_html"],
      },
    },
  });

  grunt.registerTask("default", ["dev"]);
  grunt.registerTask("dev", [
    "shell:build_html",
    "convertMarkdown",
    "sass:dev",
    "postcss:dev",
    "copy",
    "connect",
    "watch",
  ]);
  grunt.registerTask("build", [
    "shell:build_html",
    "clean:styles",
    "mkdir:styles",
    "sass:prod",
    "postcss:prod",
    "cssmin:prod",
    "copy"
  ]);

};
