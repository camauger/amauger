#!/usr/bin/env node
/**
 * Génère dist/robots.txt et y déclare le sitemap.
 *
 * Usage :
 *   node generate-robots.mjs [--dist <dossier>] [--url <https://...>] [--merge]
 *
 * Par défaut on écrit un robots.txt standard « tout autorisé + Sitemap ».
 * Avec --merge, on préserve les règles d'un robots.txt existant (cherché dans
 * public/robots.txt puis <dist>/robots.txt) et on ajoute seulement la ligne
 * Sitemap si elle manque — utile quand un projet a déjà des règles custom.
 */
import { writeFileSync, existsSync, readFileSync } from "fs"
import path from "path"
import { loadDotEnv, parseArgs, resolveDistDir, resolveSiteUrl } from "./lib.mjs"

function findExistingRobots(rootDir, distDir) {
  const candidates = [
    path.join(rootDir, "public", "robots.txt"),
    path.join(distDir, "robots.txt"),
  ]
  for (const p of candidates) {
    if (existsSync(p)) return p
  }
  return null
}

function buildStandardRobots(siteBaseUrl) {
  return (
    [
      "User-agent: *",
      "Allow: /",
      "",
      "# Généré automatiquement au build",
      `Sitemap: ${siteBaseUrl}/sitemap.xml`,
    ].join("\n") + "\n"
  )
}

function mergeRobots(existingContent, siteBaseUrl) {
  const sitemapLine = `Sitemap: ${siteBaseUrl}/sitemap.xml`
  if (/^\s*Sitemap:\s*/im.test(existingContent)) {
    // Le sitemap est déjà déclaré : on garde tel quel.
    return existingContent.endsWith("\n")
      ? existingContent
      : existingContent + "\n"
  }
  const base = existingContent.replace(/\s*$/, "")
  return base + "\n\n" + sitemapLine + "\n"
}

function main() {
  const rootDir = process.cwd()
  loadDotEnv(rootDir)
  const args = parseArgs()

  const distDir = resolveDistDir({ args, rootDir })
  const siteBaseUrl = resolveSiteUrl({ args, rootDir })
  if (!siteBaseUrl) {
    console.error(
      "[robots] URL du site inconnue. Passez --url https://exemple.com " +
        "ou définissez SITE_URL (ou VITE_SITE_URL).",
    )
    process.exit(1)
  }

  let content
  if (args.merge) {
    const existing = findExistingRobots(rootDir, distDir)
    content = existing
      ? mergeRobots(readFileSync(existing, "utf8"), siteBaseUrl)
      : buildStandardRobots(siteBaseUrl)
  } else {
    content = buildStandardRobots(siteBaseUrl)
  }

  const outPath = path.join(distDir, "robots.txt")
  writeFileSync(outPath, content, "utf8")
  console.log(`[robots] Généré : ${outPath}`)
}

main()
