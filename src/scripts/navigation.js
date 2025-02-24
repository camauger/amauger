// navigation.js
let menuToggle;
let navMenu;
let header;
let lastScroll = 0;
const scrollThreshold = 50;

/**
 * Initialise la navigation mobile et le comportement du header au scroll
 */
export function initMobileMenu() {
  // Récupération des éléments
  menuToggle = document.querySelector(".menu-toggle");
  navMenu = document.querySelector(".nav-menu");
  header = document.querySelector("header");

  if (!menuToggle || !navMenu) return;

  // Event listeners
  menuToggle.addEventListener("click", toggleMobileMenu);
  initScrollBehavior();
  initClickOutsideMenu();
  initKeyboardNavigation();
}

/**
 * Toggle le menu mobile
 */
function toggleMobileMenu() {
  const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";

  menuToggle.setAttribute("aria-expanded", !isExpanded);
  navMenu.classList.toggle("visible");

  // Gestion du scroll lock
  document.body.style.overflow = isExpanded ? "" : "hidden";
}

/**
 * Gestion du comportement au scroll
 */
function initScrollBehavior() {
  let ticking = false;

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        handleScroll();
        ticking = false;
      });
      ticking = true;
    }
  });
}

/**
 * Logique de gestion du scroll
 */
function handleScroll() {
  const currentScroll = window.pageYOffset;

  if (currentScroll > lastScroll) {
    // Scroll vers le bas
    if (currentScroll > scrollThreshold) {
      header.classList.add("header-hidden");
    }
  } else {
    // Scroll vers le haut
    header.classList.remove("header-hidden");
    header.classList.add("header-visible");
  }

  lastScroll = currentScroll;
}

/**
 * Gestion des clics en dehors du menu
 */
function initClickOutsideMenu() {
  document.addEventListener("click", (event) => {
    if (
      !event.target.closest(".main-navigation") &&
      navMenu?.classList.contains("visible")
    ) {
      closeMenu();
    }
  });
}

/**
 * Ferme le menu mobile
 */
function closeMenu() {
  menuToggle.setAttribute("aria-expanded", "false");
  navMenu.classList.remove("visible");
  document.body.style.overflow = "";
}

/**
 * Gestion de la navigation au clavier
 */
function initKeyboardNavigation() {
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navMenu?.classList.contains("visible")) {
      closeMenu();
    }
  });
}
