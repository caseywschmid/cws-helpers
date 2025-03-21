# Poetry Guide

## Overview

Poetry is a tool for **dependency management** and **packaging** in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

## Getting Started

### Installation

```bash
# Install Poetry using the official installer
curl -sSL https://install.python-poetry.org | python3 -
```

For more installation options, see the [official installation documentation](https://python-poetry.org/docs/#installation).

### First-Time Project Setup

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install dependencies
poetry install
```

This single command creates a virtual environment and installs all dependencies.

## Key Commands

| Command | Description |
|---------|-------------|
| `poetry install` | Creates virtual environment and installs dependencies |
| `poetry add <package>` | Adds a new dependency |
| `poetry add <package> --group dev` | Adds a development dependency |
| `poetry remove <package>` | Removes a dependency |
| `poetry update` | Updates dependencies to their latest versions |
| `poetry shell` | Activates the virtual environment |
| `poetry run <command>` | Runs a command within the virtual environment |
| `poetry lock` | Updates the lock file without installing packages |
| `poetry env info` | Shows information about the virtual environment |

For a complete list of commands, see the [Poetry commands documentation](https://python-poetry.org/docs/cli/).

## Virtual Environment Management

### Default Behavior

By default, Poetry creates virtual environments in a centralized location:
- Linux/macOS: `~/.cache/pypoetry/virtualenvs/`
- Windows: `%APPDATA%\pypoetry\virtualenvs/`

### Local Virtual Environment (Optional)

If you prefer having the virtual environment in your project directory:

```bash
# Configure Poetry to create virtualenvs in the project directory
poetry config virtualenvs.in-project true
```

This creates a `.venv` folder in your project directory.

For more information, see [Managing environments](https://python-poetry.org/docs/managing-environments/).

### VS Code Integration

To automatically activate the Poetry environment in VS Code:

1. **Auto-detection**: VS Code's Python extension should automatically detect Poetry environments.

2. **Find Poetry environment path**: First, determine the path to your Poetry environment:

```bash
poetry env info --path
```

3. **Manual configuration**: Create or edit `.vscode/settings.json` in your project with the path from the previous step:

```json
{
    "python.defaultInterpreterPath": "/path/to/poetry/virtualenv/bin/python",
    "python.poetryPath": "poetry",
    "python.terminal.activateEnvironment": true
}
```

If you've configured Poetry to use in-project virtual environments, you can use:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.poetryPath": "poetry",
    "python.terminal.activateEnvironment": true
}
```

## Understanding the Lock File

The `poetry.lock` file is crucial for reproducible builds:

- **Purpose**: Ensures all developers use identical dependency versions
- **Creation**: Generated automatically when running `poetry add` or `poetry lock`
- **Version Control**: Should always be committed to version control
- **Security**: Contains package hashes for integrity verification

### When to Use `poetry lock`

Run `poetry lock` when:
- You manually edit dependencies in `pyproject.toml`
- You want to update the lock file without installing packages
- You need to resolve dependency conflicts

Learn more about dependency management in the [official documentation](https://python-poetry.org/docs/dependency-specification/).

## Dependency Groups

Poetry organizes dependencies into groups:

```bash
# Install with development dependencies
poetry install --with dev

# Install without development dependencies
poetry install --without dev
```

## Advantages Over Manual pip+venv

1. **Dependency Resolution**: Automatically resolves dependency conflicts
2. **Single Configuration File**: All project metadata in `pyproject.toml`
3. **Reproducible Builds**: Lock file ensures consistent environments
4. **Simplified Workflow**: No manual virtual environment management
5. **Dependency Groups**: Organize dependencies by purpose (dev, test, etc.)

## Troubleshooting

If you encounter issues:

```bash
# Update Poetry itself
poetry self update

# Clear Poetry's cache
poetry cache clear --all .

# Debug dependency resolution
poetry install -v
```

## Additional Resources

- [Official Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry GitHub Repository](https://github.com/python-poetry/poetry)
- [Python Packaging User Guide](https://packaging.python.org/)