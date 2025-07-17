# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the enview project.

## Workflows

### 1. Lint Workflow (`lint.yml`)
- **Trigger**: On push to main branch and pull requests
- **Purpose**: Runs ruff linting and formatting checks
- **Python versions**: Tests against Python 3.8, 3.9, 3.10, 3.11, and 3.12

### 2. Build and Release Workflow (`build-release.yml`)
- **Trigger**: On push to main branch when version is updated
- **Purpose**: Automatically builds and releases new versions
- **Actions**:
  - Detects version changes in commit messages
  - Builds Python packages (wheel and sdist)
  - Creates GitHub release with artifacts
  - Publishes to PyPI (requires `PYPI_API_TOKEN` secret)

## Setup Instructions

### For PyPI Publishing
1. Create an API token on PyPI
2. Add it as a GitHub secret named `PYPI_API_TOKEN`

### Version Management
Use bumpver to manage versions:
```bash
# Install bumpver
pip install bumpver

# Bump patch version (1.0.4 -> 1.0.5)
bumpver update --patch

# Bump minor version (1.0.4 -> 1.1.0)
bumpver update --minor

# Bump major version (1.0.4 -> 2.0.0)
bumpver update --major
```

The version update will automatically trigger the build and release workflow.