#!/usr/bin/env bash
# update-index.sh — regenerate the Document Index table in Agents.md.
#
# Scans the mmark source draft for ATX headings (`#`..`######`) and rewrites the
# table between the AUTO-INDEX markers in Agents.md, in place.
#
# Usage: ./update-index.sh [path/to/draft.md]
set -euo pipefail

Agents.md="Agents.md"
BEGIN='<!-- BEGIN AUTO-INDEX -->'
END='<!-- END AUTO-INDEX -->'

# --- locate the source draft -------------------------------------------------
SRC="${1:-$(ls -1 src/draft-*.md 2>/dev/null | sort | tail -n1)}"
[ -n "${SRC:-}" ] && [ -f "$SRC" ] || { echo "source draft not found" >&2; exit 1; }

# --- sanity-check fenced-code balance ----------------------------------------
# We skip headings found *inside* fenced code blocks. That relies on every fence
# being balanced. If the source has an odd number of fence lines (a stray or
# mismatched ```), fence-tracking would desync and silently swallow real headings
# after the offending fence. In that case, warn and fall back to fence-unaware
# detection (this draft has no code-content line starting with "# ", so the
# fallback is exact here). Fix the source fence and re-run for the robust path.
FENCES=$(grep -cE '^```|^~~~' "$SRC" || true)
TRACK_FENCES=1
if [ $(( FENCES % 2 )) -ne 0 ]; then
  echo "WARNING: $SRC has an odd number of fenced-code markers ($FENCES) — " \
       "fence tracking disabled for the index; check for a stray \`\`\`." >&2
  TRACK_FENCES=0
fi

# --- build the table ---------------------------------------------------------
# Markdown/mmark heading detection: a line starting with 1-6 '#' then a space.
#   Level   = number of leading '#'.
#   Title   = heading text with a trailing "{#anchor}" stripped off.
#   Anchor  = the value inside a trailing "{#anchor}", if present.
#   Lines   = [heading line, line before the next same-or-shallower heading].
# Fenced code blocks are tracked (when balanced) so that '#' inside a ``` block is
# not mistaken for a heading.
TABLE=$(awk -v track="$TRACK_FENCES" '
  function flush(end,   pad,i,a) {
    if (have) {
      pad=""; for (i=1;i<plvl;i++) pad=pad "&nbsp;&nbsp;"
      a = (panchor=="") ? "" : "`{#" panchor "}`"
      printf "| %d | %s%s | %s | %d%s%d |\n", plvl, pad, ptitle, a, pstart, ndash, end
    }
  }
  BEGIN { ndash = "\xe2\x80\x93" }   # en-dash (U+2013), UTF-8
  (track == 1) && (/^```/ || /^~~~/) { infence = !infence; next }
  (track == 1) && infence { next }
  /^#+[ ]/ {
    line=$0
    # level = count of leading #
    n=line; sub(/[^#].*/,"",n); lvl=length(n)
    # title = text after the #s and space
    title=line; sub(/^#+[ ]+/,"",title)
    # extract trailing {#anchor}
    anchor=""
    if (match(title, /[ ]*\{#[A-Za-z0-9_-]+\}[ ]*$/)) {
      tag=substr(title, RSTART, RLENGTH)
      sub(/^[ ]*\{#/,"",tag); sub(/\}[ ]*$/,"",tag)
      anchor=tag
      sub(/[ ]*\{#[A-Za-z0-9_-]+\}[ ]*$/,"",title)
    }
    flush(NR-1)
    plvl=lvl; ptitle=title; panchor=anchor; pstart=NR; have=1
  }
  END { flush(NR) }
' "$SRC")

# --- splice into Agents.md between the markers --------------------------------
HEADER='| Level | Title | Anchor | Lines |
|-------|-------|--------|-------|'
{
  sed "/$BEGIN/q" "$Agents.md"
  printf '%s\n%s\n' "$HEADER" "$TABLE"
  sed -n "/$END/,\$p" "$Agents.md"
} > "$Agents.md.tmp" && mv "$Agents.md.tmp" "$Agents.md"

echo "Updated Document Index in $Agents.md from $SRC"
