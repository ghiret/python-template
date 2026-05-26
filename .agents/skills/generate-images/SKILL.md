---
name: generate-images
description: Generate AI documentation images using scripts/generate_doc_images.py via OpenRouter (Gemini 3 Pro Image Preview). Requires OPENROUTER_API_KEY in .env.
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Generate Images: AI-Powered Documentation Visuals

## Overview

You generate documentation images by creating markdown prompt files and running them through `scripts/generate_doc_images.py`, which calls OpenRouter's Gemini 3 Pro Image Preview model.

## The Process

### Step 1: Environment Check
1. Check that `.env` contains `OPENROUTER_API_KEY` (do NOT print the key — just confirm it exists)
2. Check that `scripts/generate_doc_images.py` exists
3. Check that `httpx` is available: `uv run python -c "import httpx"`. If missing, run `uv add httpx`.

### Step 2: Read Context
- If called from `/ralph-execute`: read the Documentation Drift Report and focus on **[GENERATE-IMAGES]** items
- If called standalone: read the user's request for what images to generate

### Step 3: Create/Update Prompt Files
Prompt files go in `docs/images/prompts/` with this format:

```markdown
# Descriptive Title

> **Target:** `docs/images/generated/filename.png`
> **Style:** Clean technical illustration, minimal color palette
> **Aspect:** 16:9 landscape

## Prompt
Detailed description of the image to generate.
Include specific details about layout, colors, labels, and style.
Be explicit about what should and should NOT appear.
```

**Naming convention:** `NN_descriptive_name.md` (e.g., `01_architecture_overview.md`)

**Guidelines for good prompts:**
- Be specific about visual layout and composition
- Specify a consistent style across related images
- Include text labels that should appear in the image
- Mention the target audience (developers, users, etc.)

### Step 4: Generate Images
1. Load environment: `set -a && source .env && set +a`
2. List available prompts: `uv run python scripts/generate_doc_images.py --list`
3. Generate specific images: `uv run python scripts/generate_doc_images.py <prompt_name>`
   - Or generate all: `uv run python scripts/generate_doc_images.py`
   - Use `--force` to regenerate existing images
4. Check output in `docs/images/generated/`

### Step 5: Verify
1. Confirm PNG files were created and have non-zero size
2. Check `docs/images/generated/_last_response.json` if generation failed — it contains the raw API response for debugging

### Step 6: Report
> "Images generated:
> 1. Created prompt: `docs/images/prompts/01_name.md`
> 2. Generated: `docs/images/generated/01_name.png` ({size} KB)
>
> **Please review the generated images visually.**"

## Critical Rules
- **Images only.** Do NOT edit text documentation or diagram scripts.
- **Never hardcode API keys.** Always load from `.env`.
- **Always use the existing script.** Do NOT call the OpenRouter API directly — use `scripts/generate_doc_images.py`.
- **Prompt files are code.** They should be committed alongside the generated images so they can be re-run.
