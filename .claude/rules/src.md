---
paths: ["src/**"]
---

# Source Code Conventions
- Type hints required on all function signatures (parameters and return types)
- Google-style docstrings on all public functions and classes
- Use `from __future__ import annotations` for forward references
- Raise specific exceptions, not bare `Exception`
- Use `logging` module, not `print()` for operational output
- Keep modules focused; prefer composition over inheritance
