#!/usr/bin/env bash
# Push PIANDT_content to both GitHub and Hugging Face.
# Remotes use ONLY your GH and HF usernames (no tokens in URLs).
# Set GH_USER, HF_USER, and optionally GITHUB_TOKEN, HF_TOKEN for password prompt.
# Usage: ./push_to_gh_and_hf.sh

set -e
cd "$(dirname "$0")"

GH_USER="${GH_USER:-2000pd3rvr}"
HF_USER="${HF_USER:-0001AMA}"

# Remotes: username only (no token in URL)
git remote remove github 2>/dev/null || true
git remote remove hf 2>/dev/null || true
git remote add github "https://${GH_USER}@github.com/${GH_USER}/PIANDT.git"
git remote add hf "https://${HF_USER}@huggingface.co/spaces/${HF_USER}/PIANDT"

# Use tokens as password when Git asks (so URL stays username-only)
askpass_script=$(mktemp)
trap "rm -f '$askpass_script'" EXIT
cat > "$askpass_script" << 'ASKPASS'
#!/bin/bash
# Git asks for "Password for 'https://USER@host':" - return the token
prompt="$1"
if [[ "$prompt" == *"github"* ]]; then
  echo "${GITHUB_TOKEN}"
elif [[ "$prompt" == *"huggingface"* ]]; then
  echo "${HF_TOKEN}"
fi
ASKPASS
chmod +x "$askpass_script"
# Git invokes GIT_ASKPASS with the prompt as first argument
export GIT_ASKPASS="$askpass_script"

if [[ -z "$GITHUB_TOKEN" ]]; then
  echo "Note: GITHUB_TOKEN not set. You will be prompted for your GitHub password (use a token)."
fi
if [[ -z "$HF_TOKEN" ]]; then
  echo "Note: HF_TOKEN not set. You will be prompted for your Hugging Face password (use a token)."
fi

echo "Pushing to GitHub (as ${GH_USER})..."
git push -u github main
echo "Pushing to Hugging Face Space (as ${HF_USER})..."
git push -u hf main --force
echo "Done."
echo "  GitHub:  https://github.com/${GH_USER}/PIANDT"
echo "  HF:      https://huggingface.co/spaces/${HF_USER}/PIANDT"