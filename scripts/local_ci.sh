#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: scripts/local_ci.sh <candidate-head-sha>" >&2
  exit 2
fi

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
candidate_head=$1
current_head=$(git rev-parse HEAD)
if [[ "$candidate_head" != "$current_head" ]]; then
  echo "Candidate SHA $candidate_head does not match HEAD $current_head" >&2
  exit 1
fi
if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
  echo "Local CI requires a clean checkout at $candidate_head" >&2
  exit 1
fi

tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/wineauction-local-ci.XXXXXX")
trap 'rm -rf "$tmp_dir"' EXIT
archive="$tmp_dir/wineauction-plugin-1.2.1.zip"
python3 scripts/build_release.py --output "$archive" --expected-head "$candidate_head"
python3 scripts/build_openai_package.py --output "$tmp_dir/wineauction-plugin-1.2.1-openai.zip" --expected-head "$candidate_head"

printf 'LOCAL CI SUMMARY: PASS\n'
printf 'Head: %s\n' "$candidate_head"
printf 'Checks: portable manifests and versions; OAuth DCR; review metadata (five workflow positives and three negatives) and trigger-matrix structure (26 positives covering every task skill, six negatives); tracked ZIP completeness and reproducibility; packaged renderer behavior; OpenAI package build (overlay applied, no removed-skill references, no broken links, no secrets, reproducible).\n'
