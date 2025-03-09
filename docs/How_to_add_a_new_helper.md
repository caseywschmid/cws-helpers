# How to add a new Helper to cws-helpers

## General

- This project uses Poetry for dependency management.
- The project follows a `src` layout, where the actual package code is in the `src/cws_helpers` directory.
- When installed, the package is available as `cws_helpers` (without the `src/` prefix).

## Package Structure

```
cws-helpers/
├── src/
│   └── cws_helpers/  # This becomes the importable package
│       ├── __init__.py
│       ├── logger/
│       │   ├── __init__.py
│       │   └── logger.py
│       └── your_new_helper/  # Your new helper goes here
│           ├── __init__.py
│           └── your_new_helper.py
└── ...
```

## Steps

1. Create a new directory in `/src/cws_helpers/<helper name>` with the name of your new helper.
2. Create an empty `__init__.py` file in the new directory.
3. Update the `pyproject.toml` file with dependencies for the new helper. While creating the new helper, you may need to install additional dependencies. Add these dependencies using the command `poetry add <dependency>`. This will automatically update the `pyproject.toml` file and the `poetry.lock` file.
4. Create a new file in the new directory with the name `<helper name>.py`. This file will contain the code for the new helper.
5. In the `<helper name>/__init__.py` file, import and expose the functionality from your helper module:
   ```python
   # src/cws_helpers/your_helper/__init__.py
   from .your_helper import YourHelperClass, your_helper_function
   
   __all__ = ['YourHelperClass', 'your_helper_function']
   ```
6. Update the `/src/cws_helpers/__init__.py` file to import the new helper if you want it available at the top level.
7. Install your package in development mode by running `poetry install`.
8. Create the documentation for the new helper in the `docs` directory.
9. Update the `README.md` file to include the new helper in the "Available Packages" section.
