#!/usr/bin/env node
/**
 * Génère dist/sitemap.xml à partir des fichiers HTML d'un build statique.
 *
 * Usage :
 *   node generate-sitemap.mjs [--dist <dossier>] [--url <https://...>] [--no-heuristics]
 *
 * Le dossier de build et l'URL sont auto-détectés si non fournis (voir lib.mjs).
 * Les heuristiques de priorité/changefreq (page d'accueil prioritaire, /tags/
 * minoré) sont désactivables avec --no-heuristics — elles restent un choix
 * éditorial, pas une vérité universelle.
 */
import { writeFileSync, statSync } from "fs"
import path from "path"
import {
  loadDotEnv,
  parseArgs,
  resolveDistDir,
  resolveSiteUrl,
  collectHtmlFiles,
  filePathToRoute,
} from "./lib.mjs"

const EXCLUDED_FILE_NAMES = new Set(["404.html"])

function applyHeuristics(routePath) {
  let priority = 0.7
  let changefreq = "weekly"
  if (routePath === "/") {
    priority = 1.0
    changefreq = "daily"
  } else if (routePath.startsWith("/tags/")) {
    priority = 0.5
  }
  return { priority, changefreq }
}

function buildSitemapXml(siteBaseUrl, urlEntries) {
  const urlNodes = urlEntries
    .map(({ loc, lastmod, changefreq, priority }) => {
      const lines = ["  <url>", `    <loc>${siteBaseUrl}${loc}</loc>`]
      if (lastmod) lines.push(`    <lastmod>${lastmod}</lastmod>`)
      if (changefreq) lines.push(`    <changefreq>${changefreq}</changefreq>`)
      if (typeof priority === "number")
        lines.push(`    <priority>${priority.toFixed(1)}</priority>`)
      lines.push("  </url>")
      return lines.join("\n")
    })
    .join("\n")

  return (
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urlNodes +
    "\n</urlset>\n"
  )
}

function main() {
  const rootDir = process.cwd()
  loadDotEnv(rootDir)
  const args = parseArgs()

  const distDir = resolveDistDir({ args, rootDir })
  const siteBaseUrl = resolveSiteUrl({ args, rootDir })
  if (!siteBaseUrl) {
    console.error(
      "[sitemap] URL du site inconnue. Passez --url https://exemple.com " +
        "ou définissez SITE_URL (ou VITE_SITE_URL).",
    )
    process.exit(1)
  }

  const useHeuristics = !args["no-heuristics"]
  const htmlFiles = collectHtmlFiles(distDir)

  const urlEntries = htmlFiles
    .filter((f) => !EXCLUDED_FILE_NAMES.has(path.basename(f)))
    .map((f) => {
      const loc = filePathToRoute(distDir, f)
      const lastmod = new Date(statSync(f).mtime).toISOString()
      const { priority, changefreq } = useHeuristics
        ? applyHeuristics(loc)
        : { priority: 0.7, changefreq: "weekly" }
      return { loc, lastmod, changefreq, priority }
    })
    .filter((e, i, arr) => arr.findIndex((x) => x.loc === e.loc) === i)
    .sort((a, b) =>
      a.loc === "/" ? -1 : b.loc === "/" ? 1 : a.loc.localeCompare(b.loc),
    )

  const xml = buildSitemapXml(siteBaseUrl, urlEntries)
  const outPath = path.join(distDir, "sitemap.xml")
  writeFileSync(outPath, xml, "utf8")
  console.log(`[sitemap] Généré : ${outPath} (${urlEntries.length} URLs)`)
}

main()
