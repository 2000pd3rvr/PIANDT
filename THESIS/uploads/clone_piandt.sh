#!/usr/bin/env bash
# Clone HF Space PIANDT into /Users/pd3rvr/Documents/pubs/mac_up
# Replace YOUR_HF_USERNAME with your actual Hugging Face username.
# If the space is private, run: export HF_TOKEN=your_token first.

set -e
TARGET="/Users/pd3rvr/Documents/pubs/mac_up"
USERNAME="${HF_SPACE_USER:-0001AMA}"  # set HF_SPACE_USER if different

mkdir -p "$TARGET"
if [[ -d "$TARGET/.git" ]]; then
  echo "Already a git repo in $TARGET - skipping clone. Pull instead: cd $TARGET && git pull"
  exit 0
fi

if [[ -n "$HF_TOKEN" ]]; then
  git clone "https://${USERNAME}:${HF_TOKEN}@huggingface.co/spaces/${USERNAME}/PIANDT" "$TARGET"
else
  git clone "https://huggingface.co/spaces/${USERNAME}/PIANDT" "$TARGET"
fi
echo "Cloned into $TARGET"
