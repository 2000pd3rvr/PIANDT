#!/usr/bin/env bash
# Create additional private Hugging Face Spaces for PIANDT excess content.
# Run once with HF_TOKEN set. Then push to each Space (see below).
# Usage: ./create_hf_excess_spaces.sh

set -e
HF_USER="${HF_USER:-0001AMA}"

if [[ -z "$HF_TOKEN" ]]; then
  echo "Error: HF_TOKEN not set. Export it first: export HF_TOKEN=hf_..."
  exit 1
fi

SPACES=(
  "PIANDT-THESIS"
  "PIANDT-thetex"
)

for name in "${SPACES[@]}"; do
  echo "Creating private Space: ${HF_USER}/${name} ..."
  out=$(curl -s -w "\n%{http_code}" -X POST "https://huggingface.co/api/repos/create" \
    -H "Authorization: Bearer ${HF_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"${name}\",\"type\":\"space\",\"private\":true,\"sdk\":\"docker\"}")
  code=$(echo "$out" | tail -1)
  body=$(echo "$out" | sed '$d')
  if [[ "$code" == "200" ]] || [[ "$body" == *"already exists"* ]] || [[ "$body" == *"name is already taken"* ]]; then
    echo "  OK: https://huggingface.co/spaces/${HF_USER}/${name}"
  else
    echo "  Response ($code): $body"
  fi
done

echo ""
echo "To push main (full repo) to one of these Spaces, add a remote and push:"
echo "  git remote add hf-thetex \"https://${HF_USER}@huggingface.co/spaces/${HF_USER}/PIANDT-thetex\""
echo "  git push hf-thetex main --force"
echo ""
echo "Note: Each Space has a 1 GB limit. If push fails with 'storage limit',"
echo "use GitHub for full content: https://github.com/2000pd3rvr/PIANDT"
