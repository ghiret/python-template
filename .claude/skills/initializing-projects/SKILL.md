# Skill: Initializing Projects

## Purpose
Transform a freshly cloned python-template into a properly configured project with the correct name, license, author information, and directory structure.

## When to Use
- After cloning the python-template repository
- When setting up a new Python project
- When the user runs the `initialize-project` command

## Workflow

### Step 1: Gather Information
Interactively collect from the user:
- Project name (validate it's a valid Python package name)
- Short description
- Author name and email
- License preference
- GitHub organization/username (optional)
- GitHub Pages deployment (default: No for private repos, Yes for public)

### Step 2: Validate Input
- Ensure package name follows PEP 8 naming conventions (lowercase, underscores)
- Ensure repo name is valid (lowercase, hyphens)
- Validate email format if provided

### Step 3: Apply Configuration

#### pyproject.toml
```toml
[project]
name = "<package_name>"
description = "<description>"
authors = [{name = "<author>", email = "<email>"}]
license = {text = "<license>"}
```

#### Directory Structure
Create if not exists:
```
plans/
docs/
docs/scratchpads/
```

#### Release Please Configuration
Update `release-please-config.json`:
```json
{
  "packages": {
    ".": {
      "package-name": "<project_name>"
    }
  }
}
```

Reset `.release-please-manifest.json` to start fresh:
```json
{
  ".": "0.1.0"
}
```

#### License File
Generate appropriate LICENSE file based on selection:
- MIT: Include year and author name
- Apache-2.0: Standard Apache license
- GPL-3.0: Standard GPL license
- BSD-3-Clause: Include year and author
- Unlicense: Public domain dedication

#### GitHub Pages (if disabled)
Modify `.github/workflows/docs.yml` to disable auto-deploy:
- Change deploy condition to only trigger on manual `workflow_dispatch` with `deploy: true`
- Docs will still build and be available as downloadable artifacts
- Users can manually trigger deployment when ready

#### mkdocs.yml
Update with project details:
```yaml
site_name: <Project Name>
repo_name: <username>/<repo>
repo_url: https://github.com/<username>/<repo>
```

### Step 4: Update References
- Update all occurrences of "python-template" to new project name
- Update package imports in any example files
- Update devcontainer name and workdir

### Step 5: Verify Setup
- Run `uv sync` to ensure dependencies install
- Run `uv run pre-commit install` to set up hooks
- Optionally run `uv run pytest` to verify test setup

## Best Practices

1. **Don't overwrite user changes**: If files appear modified, ask before overwriting
2. **Preserve template features**: Keep the .claude/ skills and commands intact
3. **Validate before applying**: Show the user what will change before making edits
4. **Create backup checkpoint**: Suggest user commits current state before initialization

## Common License Templates

### MIT
```
MIT License

Copyright (c) <year> <author>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Error Handling
- If `uv` is not installed, provide installation instructions
- If git remote fails, provide manual instructions
- If pre-commit install fails, continue but warn user
