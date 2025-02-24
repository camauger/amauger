// themeToggle.js
let themeToggle;

/**
 * Initialise le toggle du thème
 */
export function initThemeToggle() {
  // Récupération de l'élément
  themeToggle = document.querySelector(".theme-toggle");

  if (!themeToggle) return;

  // Initialisation du thème
  initializeTheme();

  // Event listener
  themeToggle.addEventListener("click", toggleTheme);

  // Observer les changements de préférence système
  watchSystemThemeChanges();
}

/**
 * Initialise le thème au chargement
 */
function initializeTheme() {
  // Récupérer le thème sauvegardé ou la préférence système
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initialTheme = savedTheme || (prefersDark ? "dark" : "light");

  // Appliquer le thème initial
  applyTheme(initialTheme);
}

/**
 * Toggle entre les thèmes sombre et clair
 */
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute("data-theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  applyTheme(newTheme);
}

/**
 * Applique un thème donné
 * @param {string} theme - Le thème à appliquer ('dark' ou 'light')
 */
function applyTheme(theme) {
  // Ajouter la classe de transition
  document.documentElement.classList.add("theme-transition");

  // Appliquer le thème
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);

  // Retirer la classe de transition après l'animation
  setTimeout(() => {
    document.documentElement.classList.remove("theme-transition");
  }, 300);
}

/**
 * Observe les changements de préférence système
 */
function watchSystemThemeChanges() {
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  mediaQuery.addEventListener("change", (e) => {
    // Ne mettre à jour que si aucun thème n'est explicitement défini
    if (!localStorage.getItem("theme")) {
      applyTheme(e.matches ? "dark" : "light");
    }
  });
}
