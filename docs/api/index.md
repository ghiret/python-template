# API Reference

This section contains auto-generated API documentation from docstrings.

## Modules

<!-- Add your module documentation here using mkdocstrings -->

<!-- Example:
::: src.your_module
    options:
      show_root_heading: true
      heading_level: 2
-->

!!! note "Getting Started"
    After initializing your project and adding code, update this file to document your modules:

    ```markdown
    ::: your_package.module_name
        options:
          show_root_heading: true
          heading_level: 2
    ```

## Docstring Style

This project uses **Google-style docstrings**:

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """Short description of the function.

    Longer description if needed. Can span multiple lines
    and include examples.

    Args:
        param1: Description of param1.
        param2: Description of param2. Defaults to 10.

    Returns:
        Description of return value.

    Raises:
        ValueError: If param1 is empty.

    Example:
        >>> example_function("hello", 20)
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return len(param1) > param2
```
