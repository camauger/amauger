// languageSwitcher.js
let langToggle;
let langMenu;

/**
 * Initialise le sélecteur de langue
 */
export function initLanguageSwitcher() {
  // Récupération des éléments
  langToggle = document.querySelector(".lang-toggle");
  langMenu = document.querySelector(".lang-menu");

  if (!langToggle || !langMenu) return;

  // Event listeners
  langToggle.addEventListener("click", toggleLanguageMenu);
  initClickOutside();
  initKeyboardNavigation();
}

/**
 * Toggle le menu des langues
 */
function toggleLanguageMenu() {
  const isExpanded = langToggle.getAttribute("aria-expanded") === "true";

  langToggle.setAttribute("aria-expanded", !isExpanded);
  langMenu.classList.toggle("visible");
}

/**
 * Gestion des clics en dehors du menu des langues
 */
function initClickOutside() {
  document.addEventListener("click", (event) => {
    if (
      !event.target.closest(".language-switcher") &&
      langMenu?.classList.contains("visible")
    ) {
      closeLanguageMenu();
    }
  });
}

/**
 * Ferme le menu des langues
 */
function closeLanguageMenu() {
  langToggle.setAttribute("aria-expanded", "false");
  langMenu.classList.remove("visible");
}

/**
 * Gestion de la navigation au clavier
 */
function initKeyboardNavigation() {
  // Gestion de la touche Échap
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && langMenu?.classList.contains("visible")) {
      closeLanguageMenu();
    }
  });

  // Navigation avec les flèches dans le menu
  const langLinks = langMenu.querySelectorAll("a");

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
