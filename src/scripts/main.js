import { initMobileMenu } from "./navigation.js";
import { initLanguageSwitcher } from "./languageSwitcher.js";
import { initThemeToggle } from "./themeToggle.js";

// Initialisation au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  initLanguageSwitcher();
  initThemeToggle();
});
