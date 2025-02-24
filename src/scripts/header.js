/**
 * header.js - Gestion des interactions du header
 * Ce script gère toutes les interactions dynamiques du header, incluant :
 * - Le menu mobile (hamburger)
 * - Le sélecteur de langue
 * - Le toggle du thème sombre/clair
 * - L'animation du header au scroll
 */

class HeaderController {
  constructor() {
    // Éléments du DOM
    this.header = document.querySelector("header");
    this.menuToggle = document.querySelector(".menu-toggle");
    this.navMenu = document.querySelector(".nav-menu");
    this.langToggle = document.querySelector(".lang-toggle");
    this.langMenu = document.querySelector(".lang-menu");
    this.themeToggle = document.querySelector(".theme-toggle");

    // État
    this.lastScroll = 0;
    this.scrollThreshold = 50; // Nombre de pixels à scroller avant de cacher le header
    this.isScrollingUp = false;

    // Initialisation
    this.init();
  }

  /**
   * Initialise tous les gestionnaires d'événements
   */
  init() {
    this.initMenuToggle();
    this.initLangSwitcher();
    this.initThemeToggle();
    this.initScrollBehavior();
    this.initClickOutside();
    this.initKeyboardNavigation();
  }

  /**
   * Gestion du menu mobile
   * - Toggle du menu au clic
   * - Animation du bouton hamburger
   * - Gestion de l'attribut aria-expanded
   */
  initMenuToggle() {
    if (!this.menuToggle) return;

    this.menuToggle.addEventListener("click", () => {
      const isExpanded =
        this.menuToggle.getAttribute("aria-expanded") === "true";

      this.menuToggle.setAttribute("aria-expanded", !isExpanded);
      this.navMenu.classList.toggle("visible");

      // Empêcher le scroll du body quand le menu est ouvert sur mobile
      document.body.style.overflow = isExpanded ? "" : "hidden";
    });
  }

  /**
   * Gestion du sélecteur de langue
   * - Toggle du menu au clic
   * - Animation du dropdown
   * - Gestion des états aria
   */
  initLangSwitcher() {
    if (!this.langToggle || !this.langMenu) return;

    this.langToggle.addEventListener("click", () => {
      const isExpanded =
        this.langToggle.getAttribute("aria-expanded") === "true";

      this.langToggle.setAttribute("aria-expanded", !isExpanded);
      this.langMenu.classList.toggle("visible");

      // Si on ouvre le menu des langues, on ferme le menu mobile
      if (!isExpanded && this.navMenu.classList.contains("visible")) {
        this.menuToggle.click();
      }
    });
  }

  /**
   * Gestion du thème sombre/clair
   * - Toggle du thème
   * - Sauvegarde de la préférence
   * - Animation des icônes
   */
  initThemeToggle() {
    if (!this.themeToggle) return;

    // Récupérer le thème sauvegardé ou utiliser la préférence système
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const currentTheme = savedTheme || (prefersDark ? "dark" : "light");

    // Appliquer le thème initial
    document.documentElement.setAttribute("data-theme", currentTheme);

    this.themeToggle.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";

      // Animer le changement de thème
      document.documentElement.classList.add("theme-transition");
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);

      // Retirer la classe d'animation après la transition
      setTimeout(() => {
        document.documentElement.classList.remove("theme-transition");
      }, 300);
    });
  }

  /**
   * Gestion du comportement au scroll
   * - Cacher/montrer le header
   * - Animations fluides
   * - Optimisation des performances
   */
  initScrollBehavior() {
    // Utiliser requestAnimationFrame pour optimiser les performances
    let ticking = false;

    window.addEventListener("scroll", () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          this.handleScroll();
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  /**
   * Logique de gestion du scroll
   * - Détection de la direction du scroll
   * - Application des classes appropriées
   */
  handleScroll() {
    const currentScroll = window.pageYOffset;

    // Détecter la direction du scroll
    if (currentScroll > this.lastScroll && !this.isScrollingUp) {
      // Scroll vers le bas
      if (currentScroll > this.scrollThreshold) {
        this.header.classList.add("header-hidden");
      }
      this.isScrollingUp = true;
    } else if (currentScroll < this.lastScroll && this.isScrollingUp) {
      // Scroll vers le haut
      this.header.classList.remove("header-hidden");
      this.header.classList.add("header-visible");
      this.isScrollingUp = false;
    }

    this.lastScroll = currentScroll;
  }

  /**
   * Gestion des clics en dehors des menus
   * Ferme les menus ouverts quand on clique ailleurs
   */
  initClickOutside() {
    document.addEventListener("click", (event) => {
      // Fermer le menu des langues si clic en dehors
      if (
        !event.target.closest(".language-switcher") &&
        this.langMenu?.classList.contains("visible")
      ) {
        this.langToggle.setAttribute("aria-expanded", "false");
        this.langMenu.classList.remove("visible");
      }

      // Fermer le menu mobile si clic en dehors
      if (
        !event.target.closest(".main-navigation") &&
        this.navMenu?.classList.contains("visible")
      ) {
        this.menuToggle.setAttribute("aria-expanded", "false");
        this.navMenu.classList.remove("visible");
        document.body.style.overflow = "";
      }
    });
  }

  /**
   * Gestion de la navigation au clavier
   * Améliore l'accessibilité en permettant la navigation via clavier
   */
  initKeyboardNavigation() {
    // Gestion de la touche Echap
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        // Fermer tous les menus ouverts
        if (this.langMenu?.classList.contains("visible")) {
          this.langToggle.click();
        }
        if (this.navMenu?.classList.contains("visible")) {
          this.menuToggle.click();
        }
      }
    });

    // Navigation dans le menu des langues avec les flèches
    if (this.langMenu) {
      const langLinks = this.langMenu.querySelectorAll("a");

      langLinks.forEach((link) => {
        link.addEventListener("keydown", (event) => {
          const index = Array.from(langLinks).indexOf(event.target);

          switch (event.key) {
            case "ArrowUp":
              event.preventDefault();
              langLinks[index - 1 || langLinks.length - 1].focus();
              break;
            case "ArrowDown":
              event.preventDefault();
              langLinks[(index + 1) % langLinks.length].focus();
              break;
          }
        });
      });
    }
  }
}

// Initialiser le contrôleur une fois que le DOM est chargé
document.addEventListener("DOMContentLoaded", () => {
  new HeaderController();
});

/**
 * Utilitaire pour détecter le support des animations CSS
 * Permet de désactiver les animations si nécessaire
 */
function supportsAnimation() {
  const element = document.createElement("div");
  return element.style.animationName !== undefined;
}

// Si les animations ne sont pas supportées, ajouter une classe au body
if (!supportsAnimation()) {
  document.body.classList.add("no-animations");
}
