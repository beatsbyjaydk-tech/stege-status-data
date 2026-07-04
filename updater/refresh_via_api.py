#!/usr/bin/env python3
"""
Weekly Stege Status data refresh via the Anthropic API (with server-side web
search). Re-researches shop hours + Stege market dates and rewrites data.json.

Runs in GitHub Actions (see .github/workflows/weekly-refresh.yml). Needs env:
  ANTHROPIC_API_KEY   (repo secret)
  MODEL               (optional, default claude-sonnet-4-6)

It is deliberately conservative: if the model's output is not valid JSON with at
least the same set of place ids, it aborts WITHOUT changing data.json.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data.json")
PROMPT = os.path.join(os.path.dirname(__file__), "UPDATE_PROMPT.md")
MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")
KEY = os.environ.get("ANTHROPIC_API_KEY")


def die(msg, code=1):
    print("refresh: " + msg)
    sys.exit(code)


def main():
    if not KEY:
        die("ANTHROPIC_API_KEY not set")

    with open(DATA, encoding="utf-8") as f:
        current = f.read()
    old = json.loads(current)
    old_ids = sorted(p["id"] for p in old["places"])

    with open(PROMPT, encoding="utf-8") as f:
        instructions = f.read()

    user = (
        instructions
        + "\n\n## Nuværende data.json\n```json\n"
        + current
        + "\n```\n\nReturnér KUN den komplette, opdaterede data.json som ét gyldigt "
        "JSON-objekt — ingen forklaring, ingen markdown-fences, kun JSON."
    )

    body = {
        "model": MODEL,
        "max_tokens": 8000,
        "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 12}],
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={
            "content-type": "application/json",
            "x-api-key": KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.load(r)
    except Exception as e:  # noqa
        die("API call failed: " + repr(e))

    # Concatenate all text blocks from the final assistant message.
    text = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
    if not text.strip():
        die("empty model response")

    # Pull the JSON object out (tolerate stray prose / fences).
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        die("no JSON object in response")
    try:
        new = json.loads(m.group(0))
    except Exception as e:  # noqa
        die("model output not valid JSON: " + repr(e))

    # Safety checks: schema + no dropped places.
    if "places" not in new or "markets" not in new or "meta" not in new:
        die("missing top-level keys")
    new_ids = sorted(p.get("id", "") for p in new["places"])
    if new_ids != old_ids:
        die("place id set changed (%s -> %s) — refusing" % (old_ids, new_ids))

    out = json.dumps(new, ensure_ascii=False, indent=2) + "\n"
    with open(DATA, "w", encoding="utf-8") as f:
        f.write(out)
    print("refresh: data.json updated (meta.updated=%s)" % new["meta"].get("updated"))


if __name__ == "__main__":
    main()
