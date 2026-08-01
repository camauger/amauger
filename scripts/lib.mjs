/**
 * Bibliothèque partagée des scripts SEO (sitemap / robots / vérification).
 *
 * Objectif : être *portable*. Aucune dépendance npm. On lit nous-mêmes un
 * éventuel fichier .env pour ne pas dépendre de `dotenv`, et on résout le
 * dossier de build et l'URL du site à partir de plusieurs sources, par ordre
 * de priorité décroissante.
 */
import { readdirSync, statSync, existsSync, readFileSync } from "fs"
import path from "path"

/**
 * Charge un fichier .env (s'il existe) dans process.env sans écraser les
 * variables déjà définies. Parseur minimal : `CLE=valeur`, lignes `#`
 * ignorées, guillemets optionnels retirés.
 */
export function loadDotEnv(rootDir = process.cwd()) {
  const envPath = path.join(rootDir, ".env")
  if (!existsSync(envPath)) return
  const raw = readFileSync(envPath, "utf8")
  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim()
    if (!trimmed || trimmed.startsWith("#")) continue
    const eq = trimmed.indexOf("=")
    if (eq === -1) continue
    const key = trimmed.slice(0, eq).trim()
    if (key in process.env) continue
    let value = trimmed.slice(eq + 1).trim()
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1)
    }
    process.env[key] = value
  }
}

/**
 * Parse les arguments CLI de la forme `--cle valeur` et `--drapeau`.
 * Retourne un objet { cle: valeur, drapeau: true }.
 */
export function parseArgs(argv = process.argv.slice(2)) {
  const args = {}
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i]
    if (!token.startsWith("--")) continue
    const key = token.slice(2)
    const next = argv[i + 1]
    if (next === undefined || next.startsWith("--")) {
      args[key] = true
    } else {
      args[key] = next
      i++
    }
  }
  return args
}

/**
 * Dossiers de build candidats par convention des générateurs statiques.
 * On retient le PREMIER qui existe et contient au moins un .html.
 */
const BUILD_DIR_CANDIDATES = [
  "dist", // Vite, Vue, Astro
  "_site", // Eleventy, Jekyll
  "public", // Hugo, Gatsby (anciens)
  "build", // SvelteKit (adapter-static), CRA, Vue-CLI
  "out", // Next.js (export statique)
  ".output/public", // Nuxt 3 (nuxi generate)
  ".vitepress/dist", // VitePress
  "site", // MkDocs
]

function containsHtml(dir) {
  try {
    const stack = [dir]
    let scanned = 0
    while (stack.length && scanned < 5000) {
      const current = stack.pop()
      for (const name of readdirSync(current)) {
        const full = path.join(current, name)
        const st = statSync(full)
        if (st.isDirectory()) stack.push(full)
        else if (name.endsWith(".html")) return true
        scanned++
      }
    }
  } catch {
    return false
  }
  return false
}

/**
 * Résout le dossier de build absolu.
 * Priorité : --dist > $SEO_DIST_DIR > auto-détection > erreur.
 * Lève une erreur explicite si rien n'est trouvé (jamais de valeur magique).
 */
export function resolveDistDir({ args = {}, rootDir = process.cwd() } = {}) {
  const explicit = args.dist || process.env.SEO_DIST_DIR
  if (explicit) {
    const abs = path.resolve(rootDir, explicit)
    if (!existsSync(abs)) {
      throw new Error(
        `[seo] Dossier de build introuvable : ${abs}. Lancez d'abord le build, ou corrigez --dist.`,
      )
    }
    return abs
  }
  for (const candidate of BUILD_DIR_CANDIDATES) {
    const abs = path.resolve(rootDir, candidate)
    if (existsSync(abs) && containsHtml(abs)) return abs
  }
  throw new Error(
    "[seo] Impossible de détecter le dossier de build. Lancez le build du site, " +
      "puis passez --dist <dossier> (ex. dist, _site, public, build, out).",
  )
}

/**
 * Résout l'URL publique du site, sans barre finale.
 * Priorité : --url > $SITE_URL > $VITE_SITE_URL > package.json "homepage".
 * Retourne null si rien de valide n'est trouvé (l'appelant décide quoi faire).
 */
export function resolveSiteUrl({ args = {}, rootDir = process.cwd() } = {}) {
  const candidates = [
    args.url,
    process.env.SITE_URL,
    process.env.VITE_SITE_URL,
    readPackageHomepage(rootDir),
  ]
  for (const value of candidates) {
    if (value && /^https?:\/\//.test(value)) return value.replace(/\/$/, "")
  }
  return null
}

function readPackageHomepage(rootDir) {
  const pkgPath = path.join(rootDir, "package.json")
  if (!existsSync(pkgPath)) return null
  try {
    const pkg = JSON.parse(readFileSync(pkgPath, "utf8"))
    return typeof pkg.homepage === "string" ? pkg.homepage : null
  } catch {
    return null
  }
}

/**
 * Collecte récursivement tous les fichiers .html sous un dossier.
 */
export function collectHtmlFiles(rootDirectoryPath) {
  const collected = []
  function walk(dir) {
    for (const name of readdirSync(dir)) {
      const full = path.join(dir, name)
      const st = statSync(full)
      if (st.isDirectory()) walk(full)
      else if (st.isFile() && name.endsWith(".html")) collected.push(full)
    }
  }
  walk(rootDirectoryPath)
  return collected
}

/**
 * Convertit un chemin de fichier HTML en route URL propre.
 *   dist/index.html        -> /
 *   dist/blog/index.html   -> /blog/
 *   dist/about.html        -> /about
 */
export function filePathToRoute(distDir, absoluteHtmlPath) {
  const rel = path.relative(distDir, absoluteHtmlPath)
  const normalized = rel.split(path.sep).join("/")
  if (normalized === "index.html") return "/"
  if (normalized.endsWith("/index.html")) {
    return "/" + normalized.replace(/\/index\.html$/, "") + "/"
  }
  if (normalized.endsWith(".html")) {
    return "/" + normalized.replace(/\.html$/, "")
  }
  return "/" + normalized
}
