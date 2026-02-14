#!/usr/bin/env bash
# Push PIANDT_content to both GitHub and Hugging Face.
# Run from a terminal where you have exported GITHUB_TOKEN and HF_TOKEN.
# Usage: ./push_to_gh_and_hf.sh

set -e
cd "$(dirname "$0")"

GH_USER="${GH_USER:-2000pd3rvr}"
HF_USER="${HF_USER:-0001AMA}"

if [[ -z "$GITHUB_TOKEN" ]]; then
  echo "Error: GITHUB_TOKEN not set. Export it first: export GITHUB_TOKEN=ghp_..."
  exit 1
fi
if [[ -z "$HF_TOKEN" ]]; then
  echo "Error: HF_TOKEN not set. Export it first: export HF_TOKEN=hf_..."
  exit 1
fi

# Set remotes with token auth (overwrites any existing URLs)
git remote remove github 2>/dev/null || true
git remote remove hf 2>/dev/null || true
git remote add github "https://${GH_USER}:${GITHUB_TOKEN}@github.com/${GH_USER}/PIANDT.git"
git remote add hf "https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/${HF_USER}/PIANDT"

echo "Pushing to GitHub..."
git push -u github main
echo "Pushing to Hugging Face Space..."
# Force-push so Space matches local content (HF creates an initial commit when Space is created)
git push -u hf main --force
echo "Done. Both remotes updated."
echo "  GitHub:  https://github.com/${GH_USER}/PIANDT"
echo "  HF:      https://huggingface.co/spaces/${HF_USER}/PIANDT"