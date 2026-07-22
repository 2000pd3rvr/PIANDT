---
title: PIANDT
emoji: 🔬
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "4.1"
app_port: 7860
pinned: false
---

PIANDT site **v4.1** — Collaborate menu and enquiry form. Served via Docker on port 7860.

**Public repositories**

- **GitHub:** [2000pd3rvr/PIANDT](https://github.com/2000pd3rvr/PIANDT)
- **Hugging Face Space:** [0001AMA/PIANDT](https://huggingface.co/spaces/0001AMA/PIANDT)

## Versioning

Each deployment bumps a **sub-version** of the Space/site release (e.g. `4` → `4.1`). Asset cache busts follow the same release (`styles.css?v=63`, `script.js?v=30` for v4.1).

## Collaborate

Open to **local and international** partnerships. The enquiry form on `collaborate.html` will forward to an admin email once configured (`window.PIANDT_ADMIN_EMAIL` / `PIANDT_ADMIN_EMAIL` in `script.js`). Until then, submissions are stored locally as a placeholder.

## Additional Spaces (excess / archives)

Because this Space has a 1 GB storage limit, extra content may live in separate Hugging Face Spaces:

| Space | Contents |
|-------|----------|
| **PIANDT-THESIS** | THESIS folder |
| **PIANDT-thetex** | thetex manuscript sources |

Create / push those with `create_hf_excess_spaces.sh` when needed.
