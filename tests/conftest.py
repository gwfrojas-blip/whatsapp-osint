"""Shared pytest fixtures and configuration."""
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest  # pyright: ignore[reportMissingImports]
## Overview

`reportMissingImports` is a diagnostic in Pylance and Pyright that warns when an import statement cannot be resolved because the module is missing or not installed. This helps catch missing dependencies and configuration issues, improving code reliability and maintainability.

## Representative Issues

- [#2202](https://github.com/microsoft/pylance-release/issues/2202): Ensure all necessary modules are installed in the Python environment specified for the project.
- [#2996](https://github.com/microsoft/pylance-release/issues/2996): Use comments to suppress specific warnings in static analysis tools when dealing with optional imports.
- [#4976](https://github.com/microsoft/pylance-release/issues/4976): Ensure that static analysis tools are configured correctly to recognize all necessary modules, or use runtime checks if dynamic imports are involved.

## Examples

```python
import my_custom_module  # Error: Import "my_custom_module" could not be resolved
from utils import helper # Error: Import "utils" could not be resolved
```

**Fix — install the package or configure extra paths:**

```bash
# If it's a third-party library, install it:
pip install my_custom_module
```

```json
// If it's your own code in a non-standard location, add to .vscode/settings.json:
{
    "python.analysis.extraPaths": ["./src", "./lib"]
}
```

**Fix — suppress for optional/platform-specific imports:**

```python
try:
    import optional_module  # pyright: ignore[reportMissingImports]
except ImportError:
    optional_module = None
```

## Common Fixes & Workarounds

1. Install missing modules using pip or your package manager.
2. Check that the correct [Python environment](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter) is selected in your IDE or editor.
3. Use comments like `# pyright: ignore[reportMissingImports]` to suppress warnings for optional or platform-specific imports.
4. Review the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportMissingImports) for options to adjust or suppress this diagnostic if needed.

## See Also

- [Fixing unresolved imports](../howto/unresolved-imports.md) — comprehensive guide for resolving import issues
- [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) — add extra search paths for imports
- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default
"""Shared pytest fixtures and configuration for tests.

This file provides common test fixtures used across the test suite.
"""
@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_selenium_webdriver():
    """Mock Selenium WebDriver for testing."""
    with patch('selenium.webdriver.Chrome') as mock_driver:
        driver_instance = Mock()
        mock_driver.return_value = driver_instance
        yield driver_instance


@pytest.fixture
def mock_database():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        db_path = tmp_db.name
    yield db_path
    # Cleanup
    try:
        os.unlink(db_path)
    except FileNotFoundError:
        pass
## Overview

`reportUnusedExpression` is a Pylance and Pyright diagnostic that warns when an expression in your code has no effect and its result is not used. Removing unused expressions helps keep your code clean and can prevent confusion or subtle bugs.

## Representative Issues

- [#4163](https://github.com/microsoft/pylance-release/issues/4163): Ensure consistency in the use of type stubs between Pyright's CLI and Pylance settings, especially with `useLibraryCodeForTypes`.
- [#5200](https://github.com/microsoft/pylance-release/issues/5200): Provide a configuration setting to allow users to customize diagnostic rule severities based on the type checking mode, improving the granularity of error reporting.
- [#4286](https://github.com/microsoft/pyright/issues/4286): Ensure that Protocol classes are consistently imported from the `typing_extensions` module to avoid runtime issues with static type checkers.
- [#4367](https://github.com/microsoft/pyright/issues/4367): Ensure that comments in TOML files use the correct line endings and do not contain unsupported control characters to avoid parse errors.
- [#7087](https://github.com/microsoft/pyright/issues/7087): Ensure that generators are utilized in iterable contexts or explicitly stopped to avoid unused code.
- [#9236](https://github.com/microsoft/pyright/issues/9236): Ensure that static type checkers like `pyright` correctly interpret the types in the standard library, especially when there are updates or corrections in newer Python versions.
- [#9237](https://github.com/microsoft/pyright/issues/9237): Always follow the correct syntax for comments in directives to avoid errors with static type checkers like Pyright.

## Examples

**Error:**

```python
x = 10
x == 5   # Comparison result is not used (did you mean x = 5?)
-4       # Negation result is not used
```

**Fix — use the expression or remove it:**

```python
x = 10
if x == 5:     # Use in a condition
    pass
result = -4    # Assign the value
```

## Common Fixes & Workarounds

1. Remove expressions whose results are not used.
2. Assign the result to a variable if you intend to use it later.
3. Ensure generators and iterables are used in a meaningful context.
4. Use correct syntax for comments and directives.
5. Refer to the [Pyright configuration documentation](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportUnusedExpression) for details on configuring or disabling this diagnostic.

## See Also

- [`python.analysis.diagnosticSeverityOverrides`](../settings/python_analysis_diagnosticSeverityOverrides.md) — adjust or suppress this diagnostic
- [`python.analysis.typeCheckingMode`](../settings/python_analysis_typeCheckingMode.md) — controls which diagnostics are enabled by default

@pytest.fixture
def mock_excel_file(temp_dir):
    """Create a temporary Excel file path for testing."""
    return temp_dir / "test_workbook.xlsx"


@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        'chrome_driver_path': '/path/to/chromedriver',
        'database_path': 'test_victims_logs.db',
        'excel_file': 'test_history.xlsx',
        'timeout': 30,
    }


@pytest.fixture
def mock_keyboard():
    """Mock keyboard module for testing."""
    with patch('keyboard.is_pressed') as mock_is_pressed:
        mock_is_pressed.return_value = False
        yield mock_is_pressed


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset module imports between tests to ensure isolation."""
    import sys
    modules_to_reset = [
        key for key in sys.modules.keys() 
        if key.startswith('utils') or key == 'whatsappbeacon'
    ]
    for module in modules_to_reset:
        sys.modules.pop(module, None)


@pytest.fixture
def capture_logs():
    """Capture log outputs during tests."""
    import logging
    from io import StringIO
    
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.DEBUG)
    
    # Get root logger
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    yield log_capture
    
    # Cleanup
    logger.removeHandler(handler)


def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    ) # type: ignore