#!/usr/bin/env node
/**
 * Vérifie et audite la préparation SEO d'un build statique. Aucun appel réseau.
 *
 * Usage :
 *   node verify-seo.mjs [--dist <dossier>] [--url <https://...>] [--max-report <n>]
 *
 * Trois familles de contrôles :
 *   1. Fichiers   : sitemap.xml + robots.txt présents, robots référence le sitemap.
 *   2. Sitemap    : XML bien formé, comptage d'URLs, doublons, cohérence du
 *                   domaine, limites du protocole (50 000 URLs / 50 Mo).
 *   3. On-page    : chaque HTML a-t-il <title>, meta description, canonical et
 *                   les balises Open Graph de base (og:title/description/image).
 *
 * Sortie : un rapport lisible + un code de sortie non nul si un contrôle
 * *bloquant* échoue (fichiers manquants). Les manques on-page sont des
 * avertissements : ils n'empêchent pas l'indexation mais la dégradent.
 *
 * Rappel : Google et Bing ont retiré le ping HTTP de sitemap en 2023. La
 * découverte passe par robots.txt, Search Console / Bing Webmaster et le crawl.
 * @see https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
 */
import { existsSync, readFileSync, statSync } from "fs"
import path from "path"
import {
  loadDotEnv,
  parseArgs,
  resolveDistDir,
  resolveSiteUrl,
  collectHtmlFiles,
} from "./lib.mjs"

const SITEMAP_MAX_URLS = 50000
const SITEMAP_MAX_BYTES = 50 * 1024 * 1024

let hardFailure = false
const warn = (msg) => console.log(`  ⚠ ${msg}`)
const ok = (msg) => console.log(`  ✓ ${msg}`)
const fail = (msg) => {
  hardFailure = true
  console.log(`  ✗ ${msg}`)
}

function checkFiles(distDir) {
  console.log("\n[1/3] Fichiers")
  const sitemapPath = path.join(distDir, "sitemap.xml")
  const robotsPath = path.join(distDir, "robots.txt")

  if (existsSync(sitemapPath)) ok(`sitemap.xml présent`)
  else fail(`sitemap.xml absent — lancez generate-sitemap.mjs`)

  if (existsSync(robotsPath)) {
    ok(`robots.txt présent`)
    const robots = readFileSync(robotsPath, "utf8")
    if (/^\s*Sitemap:\s*/im.test(robots)) ok(`robots.txt référence le sitemap`)
    else warn(`robots.txt ne déclare pas de ligne Sitemap:`)
    if (/^\s*Disallow:\s*\/\s*$/im.test(robots))
      warn(`robots.txt contient "Disallow: /" — tout le site est bloqué !`)
  } else {
    fail(`robots.txt absent — lancez generate-robots.mjs`)
  }

  return { sitemapPath, robotsPath }
}

function checkSitemap(sitemapPath, siteBaseUrl) {
  console.log("\n[2/3] Sitemap")
  if (!existsSync(sitemapPath)) {
    warn("sitemap.xml absent — contrôles sautés")
    return
  }

  const bytes = statSync(sitemapPath).size
  const xml = readFileSync(sitemapPath, "utf8")

  if (!/<urlset[\s>]/.test(xml) || !/<\/urlset>/.test(xml)) {
    fail("XML mal formé : <urlset> introuvable")
    return
  }
  ok("structure <urlset> présente")

  const locs = [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map((m) => m[1].trim())
  ok(`${locs.length} URL(s)`)

  if (locs.length > SITEMAP_MAX_URLS)
    fail(`${locs.length} URLs > limite ${SITEMAP_MAX_URLS} (découper en index)`)
  if (bytes > SITEMAP_MAX_BYTES)
    fail(`${(bytes / 1048576).toFixed(1)} Mo > limite 50 Mo`)

  const seen = new Set()
  const dups = new Set()
  for (const loc of locs) {
    if (seen.has(loc)) dups.add(loc)
    seen.add(loc)
  }
  if (dups.size) warn(`${dups.size} URL(s) en double (ex. ${[...dups][0]})`)
  else ok("aucun doublon")

  if (siteBaseUrl) {
    const offDomain = locs.filter((l) => !l.startsWith(siteBaseUrl))
    if (offDomain.length)
      warn(
        `${offDomain.length} URL(s) hors du domaine ${siteBaseUrl} (ex. ${offDomain[0]})`,
      )
    else ok(`toutes les URLs sur ${siteBaseUrl}`)
  }
}

function auditPage(html) {
  const missing = []
  if (!/<title[^>]*>\s*\S/i.test(html)) missing.push("title")
  if (!/<meta[^>]+name=["']description["'][^>]+content=["']\s*\S/i.test(html))
    missing.push("meta description")
  if (!/<link[^>]+rel=["']canonical["']/i.test(html)) missing.push("canonical")
  if (!/<meta[^>]+property=["']og:title["']/i.test(html))
    missing.push("og:title")
  if (!/<meta[^>]+property=["']og:description["']/i.test(html))
    missing.push("og:description")
  if (!/<meta[^>]+property=["']og:image["']/i.test(html))
    missing.push("og:image")
  return missing
}

function checkOnPage(distDir, maxReport) {
  console.log("\n[3/3] Audit on-page")
  const files = collectHtmlFiles(distDir).filter(
    (f) => path.basename(f) !== "404.html",
  )
  if (!files.length) {
    warn("aucun fichier HTML trouvé")
    return
  }

  const tally = {}
  const problems = []
  for (const f of files) {
    const missing = auditPage(readFileSync(f, "utf8"))
    for (const m of missing) tally[m] = (tally[m] || 0) + 1
    if (missing.length)
      problems.push({ route: path.relative(distDir, f), missing })
  }

  ok(`${files.length} page(s) analysée(s)`)
  if (!problems.length) {
    ok("toutes les balises SEO de base sont présentes")
    return
  }

  console.log("  Manques par balise :")
  for (const [tag, count] of Object.entries(tally).sort((a, b) => b[1] - a[1])) {
    console.log(`    - ${tag} : ${count} page(s)`)
  }
  console.log(`  Pages concernées (max ${maxReport}) :`)
  for (const p of problems.slice(0, maxReport)) {
    console.log(`    - ${p.route} → manque : ${p.missing.join(", ")}`)
  }
  if (problems.length > maxReport)
    console.log(`    … et ${problems.length - maxReport} autre(s).`)
}

function main() {
  const rootDir = process.cwd()
  loadDotEnv(rootDir)
  const args = parseArgs()
  const maxReport = Number(args["max-report"]) || 20

  const distDir = resolveDistDir({ args, rootDir })
  const siteBaseUrl = resolveSiteUrl({ args, rootDir })

  console.log(`[seo] Vérification du build : ${distDir}`)
  console.log(`[seo] URL publique : ${siteBaseUrl || "(inconnue)"}`)

  const { sitemapPath } = checkFiles(distDir)
  checkSitemap(sitemapPath, siteBaseUrl)
  checkOnPage(distDir, maxReport)

  console.log("\n[seo] Soumission : Google Search Console / Bing Webmaster Tools.")
  console.log("[seo] (Le ping HTTP Google/Bing a été retiré en 2023.)")

  if (hardFailure) {
    console.log("\n[seo] Échec : des fichiers indispensables manquent.")
    process.exit(1)
  }
  console.log("\n[seo] OK.")
}

main()
