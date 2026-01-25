# Initialize Project

Initialize this project from the python-template. Gather the following information from the user, then apply the changes.

## Required Information

Ask the user for:

1. **Project Name** (snake_case for package, kebab-case for repo)
   - Example: `my_awesome_project` / `my-awesome-project`

2. **Description** (one-line summary)

3. **Author Name** and **Email**

4. **License** (default: MIT)
   - Options: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, Unlicense, None
   - Note: This template is MIT licensed, but your project can use any license

5. **GitHub Username/Org** (for repository URL)

6. **GitHub Pages** (default: No for private repos)
   - Ask: "Is this a public repository that should deploy docs to GitHub Pages?"
   - If No: Disable auto-deploy in `.github/workflows/docs.yml`

## Actions to Perform

After gathering information:

1. **Update `pyproject.toml`:**
   - Set `name` to the package name (snake_case)
   - Set `description`
   - Set `version = "0.1.0"` (reset for new project)
   - Add `authors = [{name = "...", email = "..."}]`
   - Add `license = {text = "..."}` if specified
   - Update `[tool.ruff.lint.isort] known-first-party`

2. **Rename `src/` package:**
   - Rename `src/` to the package name OR
   - Create `src/<package_name>/` structure based on user preference

3. **Update `README.md`:**
   - Replace title and description
   - Update installation instructions with correct package name
   - Add license badge if applicable

4. **Update `.devcontainer/devcontainer.json`:**
   - Update the `"name"` field

5. **Update `.devcontainer/Dockerfile`:**
   - Update `WORKDIR` to use new project name

6. **Update `release-please-config.json`:**
   - Set `package-name` to the new project name

7. **Reset `.release-please-manifest.json`:**
   - Reset version to `"0.1.0"` for fresh start

8. **Update `.github/workflows/docs.yml`** (if GitHub Pages disabled):
   - Change the deploy condition to only run on `workflow_dispatch` with `inputs.deploy == true`
   - This keeps docs building as artifacts but doesn't auto-publish

9. **Update `mkdocs.yml`:**
   - Set `site_name` to project name
   - Update `repo_name` and `repo_url` with GitHub username/org

10. **Create `LICENSE` file** (if license selected)

11. **Create required directories:**
   - `plans/`
   - `docs/scratchpads/`

10. **Initialize git remote** (if GitHub username provided):
    - Suggest: `git remote set-url origin git@github.com:<user>/<repo>.git`

11. **Run initial setup:**
    - `uv sync --all-extras`
    - `uv run pre-commit install`

## Output

After completion, summarize what was configured and remind the user to:
- Review the changes
- Commit the initialization: `git add -A && git commit -m "chore: initialize project from template"`
- Push to their repository
