# HTML Artifact Conventions

These conventions define how skills create, read, and exchange agent-produced
artifacts. HTML is the preferred artifact format because it is persistent,
readable outside the agent session, and structured enough for reliable parsing.
Markdown remains fully supported for existing plans and workflows.

## Artifact Locations

- Plans: `agent_docs/plans/*.html`
- Plan reviews: `agent_docs/reports/reviews/*.html`
- Verification reports: `agent_docs/reports/verify/*.html`
- Documentation drift reports: `agent_docs/reports/drift/*.html`
- Scratch, research, imported API docs, and temporary references: `agent_docs/`
- External source documentation snapshots: `external_docs/`

Generated reports and scratch artifacts belong under `agent_docs/` and should
not be committed unless the user explicitly asks for them.

## Executable HTML Plan Schema

An executable HTML plan MUST be self-contained and use this structure:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Feature Plan</title>
  <style>
    body { font-family: system-ui, sans-serif; line-height: 1.5; }
    code { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }
  </style>
</head>
<body>
  <main data-artifact="plan" data-version="1">
    <h1>Feature Plan</h1>

    <section data-phase="1" data-title="Set up models">
      <h2>Phase 1: Set up models</h2>
      <ul class="tasks">
        <li>Create the model.</li>
        <li>Add focused tests.</li>
      </ul>
      <section class="verification">
        <h3>Verification</h3>
        <ul>
          <li><code>uv run pytest tests/models</code></li>
        </ul>
      </section>
    </section>
  </main>
</body>
</html>
```

Parsing rules:

- Each phase is a `<section>` with `data-phase="N"` and `data-title="..."`.
- Phase order follows numeric `data-phase` order unless the user requests a
  subset explicitly.
- Tasks come from `<ul class="tasks"><li>...</li></ul>` inside the phase.
- Verification steps come from `<section class="verification">`.
- Preserve code paths, commands, acceptance criteria, and architecture notes.
- Inline CSS is allowed. Do not require JavaScript, browser automation, remote
  assets, or external dependencies.

## Markdown Plan Compatibility

Markdown plans remain valid. A markdown executable plan uses:

```markdown
## Phase N: Title
- [ ] Task description

### Verification
- Specific test command or check
```

Skills that parse plans MUST support both `.html` and `.md` inputs. For `.html`
plans, use the HTML schema above. For `.md` plans, use the legacy markdown phase
headings and task checkbox format.

## HTML Report Skeleton

Review, verification, and drift reports should be written as self-contained HTML
using this skeleton:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Report Title</title>
  <style>
    body { font-family: system-ui, sans-serif; line-height: 1.5; margin: 2rem; }
    .status-pass { color: #116329; }
    .status-fail { color: #b42318; }
    code { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; }
  </style>
</head>
<body>
  <main data-artifact="report" data-report-type="review" data-version="1">
    <h1>Report Title</h1>
    <section>
      <h2>Status</h2>
      <p><strong>Review Status:</strong> APPROVED</p>
    </section>
  </main>
</body>
</html>
```

Report rules:

- Store review reports under `agent_docs/reports/reviews/`.
- Store verification reports under `agent_docs/reports/verify/`.
- Store documentation drift reports under `agent_docs/reports/drift/`.
- Use stable text/code markers for downstream parsing, such as
  `Review Status: APPROVED`, `VERIFICATION PASSED`, `[FIX-DOCS]`,
  `[GENERATE-DIAGRAMS]`, and `[GENERATE-IMAGES]`.
- Include enough source paths, commands, and findings for another agent to act
  without relying on conversation history.
