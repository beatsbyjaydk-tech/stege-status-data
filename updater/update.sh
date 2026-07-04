#!/usr/bin/env bash
# Weekly Stege Status data refresh. Runs on any always-on machine that has
# Claude Code (`claude`) + git authenticated for this repo (e.g. Jay's Mac mini
# via launchd, or a self-hosted runner). Re-researches hours + markets and pushes.
set -euo pipefail
cd "$(dirname "$0")/.."   # repo root

git pull --rebase --autostash -q origin main || true

# Let headless Claude re-research and rewrite data.json in place.
claude -p "$(cat updater/UPDATE_PROMPT.md)" --permission-mode acceptEdits 2>&1 | tail -30 || {
  echo "claude run failed"; exit 1;
}

if git diff --quiet -- data.json; then
  echo "No data changes ($(date +%F))."
else
  git add data.json
  git commit -q -m "Weekly data refresh $(date +%F)"
  git push -q origin main && echo "Pushed refreshed data.json"
fi
