# CI/CD Workflow Documentation

**Last Updated**: 2025-01-15  
**Status**: ✅ **GitHub Actions Workflow Active**

## Overview

applyr uses GitHub Actions for continuous integration, automatically running code quality checks, tests, and security scans on every push to any branch. The workflow ensures code quality standards are maintained and provides comprehensive coverage reporting.

## Workflow Configuration

### Location

- **Workflow File**: `.github/workflows/tests.yml`
- **Trigger**: All branches, on every push
- **Platform**: Ubuntu Latest
- **Python Version**: 3.9

### Workflow Structure

```yaml
name: CI Tests

on:
  push:
    branches: ['**']  # All branches

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    steps:
      # Setup, dependency installation, quality checks, test execution
```

## Automated Checks

### 1. Code Setup

**Checkout Code:**
```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

**Python Setup:**
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.9'
    cache: 'poetry'
```

**Poetry Installation:**
```yaml
- name: Install Poetry
  uses: snok/install-poetry@v1
  with:
    version: latest
    virtualenvs-create: true
    virtualenvs-in-project: true
```

### 2. Dependency Management

**Caching:**
- Poetry dependencies cached for faster builds
- Cache key based on OS, Python version, and `poetry.lock` hash
- Restores cache on subsequent runs

**Installation:**
```yaml
- name: Install dependencies
  run: poetry install --no-interaction --no-root
  if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'

- name: Install project
  run: poetry install --no-interaction
```

### 3. Code Quality Checks

**Linting (Ruff):**
```yaml
- name: Run linting
  run: poetry run ruff check .
```

- Checks code style, formatting, and common issues
- Fails workflow if linting errors are found
- See [LINTING_FORMATTING_STATUS.md](./LINTING_FORMATTING_STATUS.md) for details

**Type Checking (mypy):**
```yaml
- name: Run type checking
  run: poetry run mypy applyr/
```

- Validates type annotations
- Gradual typing approach (strict mode for new code)
- Catches type-related bugs before runtime

**Security Scanning (Bandit):**
```yaml
- name: Run security scan
  run: poetry run bandit -r applyr/ -f json -o bandit-report.json || true
```

- Scans for security vulnerabilities
- Generates JSON report for artifact upload
- Uses `|| true` to prevent workflow failure (warnings only)

### 4. Test Execution

**Test Run:**
```yaml
- name: Run tests with coverage
  run: poetry run pytest --cov=applyr --cov-report=html --cov-report=term-missing --cov-report=xml
```

- Runs full test suite with pytest
- Generates coverage reports in multiple formats:
  - **HTML**: `htmlcov/` directory (browser-viewable)
  - **Terminal**: Inline coverage in logs
  - **XML**: `coverage.xml` (CI integration)

**Coverage Configuration:**
- Source: `applyr/` directory
- Excludes: `tests/*`, `__pycache__/*`, `__init__.py`
- Target: 50%+ overall coverage

See [TESTING.md](./TESTING.md) for detailed test documentation.

### 5. Artifact Generation

**Coverage Reports:**
```yaml
- name: Upload coverage reports
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: coverage-reports
    path: |
      htmlcov/
      coverage.xml
    retention-days: 30
```

- Uploads HTML and XML coverage reports
- Available for download from GitHub Actions UI
- Retained for 30 days

**Security Report:**
```yaml
- name: Upload security report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: security-report
    path: bandit-report.json
    retention-days: 30
```

- Uploads Bandit security scan results
- Available for download and review
- Retained for 30 days

## Workflow Behavior

### Triggers

**Push Events:**
- Triggers on **all branches** (`branches: ['**']`)
- Runs on every push to any branch
- Ensures all code changes are validated

**Manual Triggers:**
- Can be manually triggered from GitHub Actions UI
- Useful for testing workflow changes

### Failure Handling

**Quality Gate Failures:**
- Linting errors: Workflow fails
- Type checking errors: Workflow fails
- Test failures: Workflow fails
- Security warnings: Workflow continues (warnings only)

**Artifact Upload:**
- Uses `if: always()` to upload artifacts even on failure
- Allows inspection of coverage and security reports even when tests fail

### Caching Strategy

**Poetry Dependencies:**
- Cache key: `poetry-{os}-{python-version}-{poetry.lock-hash}`
- Cache paths:
  - `.venv/` (virtual environment)
  - `~/.cache/pypoetry` (Poetry cache)

**Cache Benefits:**
- Faster workflow execution (2-5 minutes vs 5-10 minutes)
- Reduces load on package repositories
- More reliable builds

## Local Development Workflow

### Running CI Checks Locally

**All Checks:**
```bash
make all
```

**Individual Checks:**
```bash
make lint          # Ruff linting
make type-check    # mypy type checking
make security      # Bandit security scan
make test          # pytest with coverage
```

**Pre-commit Hooks:**
```bash
make install       # Install pre-commit hooks
pre-commit run --all-files  # Run all hooks
```

### Matching CI Environment

**Python Version:**
- CI uses Python 3.9
- Ensure local development uses Python 3.9+

**Dependencies:**
- Use `poetry install` to match CI environment
- Poetry lock file ensures consistent versions

**Commands:**
- Run same commands locally as in CI:
  ```bash
  poetry run ruff check .
  poetry run mypy applyr/
  poetry run bandit -r applyr/
  poetry run pytest --cov=applyr --cov-report=html --cov-report=term-missing --cov-report=xml
  ```

## Viewing Results

### GitHub Actions UI

**Workflow Runs:**
1. Navigate to repository
2. Click "Actions" tab
3. Select workflow run
4. Review job status and logs

**Artifacts:**
1. Open completed workflow run
2. Scroll to "Artifacts" section
3. Download `coverage-reports` or `security-report`
4. Extract and view HTML coverage report

### Coverage Reports

**HTML Report:**
- Open `htmlcov/index.html` in browser
- Interactive coverage visualization
- Line-by-line coverage details
- File and module summaries

**Terminal Report:**
- Displayed in workflow logs
- Shows coverage percentage per module
- Highlights missing lines

**XML Report:**
- `coverage.xml` for CI integration
- Can be used with coverage services
- Machine-readable format

## Troubleshooting

### Common Issues

**Workflow Fails on Linting:**
- Run `poetry run ruff check .` locally
- Fix linting errors before pushing
- Use `ruff check --fix .` to auto-fix issues

**Workflow Fails on Type Checking:**
- Run `poetry run mypy applyr/` locally
- Fix type annotation errors
- Check `pyproject.toml` for mypy configuration

**Tests Fail:**
- Run `poetry run pytest` locally
- Review test output for specific failures
- Check test fixtures and dependencies

**Cache Issues:**
- Clear cache in GitHub Actions UI if needed
- Workflow will rebuild cache on next run
- Check cache key format matches

**Dependency Installation Fails:**
- Verify `poetry.lock` is up to date
- Check Python version matches (3.9)
- Review Poetry installation logs

### Debugging Workflow

**View Logs:**
- Expand each step to see detailed output
- Check for error messages in logs
- Review artifact uploads

**Local Testing:**
- Run same commands locally as in CI
- Use Docker to match CI environment exactly
- Test workflow changes in feature branch

**Workflow Validation:**
- Use GitHub Actions YAML validator
- Check syntax with `yaml-lint` or similar
- Test workflow changes carefully

## Best Practices

### Before Pushing

1. **Run local checks:**
   ```bash
   make all
   ```

2. **Fix any errors:**
   - Linting errors
   - Type checking errors
   - Test failures

3. **Review changes:**
   - Ensure tests cover new code
   - Update documentation if needed
   - Check coverage impact

### Commit Messages

- Use clear, descriptive commit messages
- Reference issues if applicable
- Mention breaking changes

### Branch Strategy

- Workflow runs on all branches
- Feature branches get same validation
- Main branch should always pass

### Coverage Goals

- Aim for 50%+ overall coverage
- Focus on critical paths
- Add tests for new features

## Future Enhancements

### Potential Improvements

- **Matrix Testing**: Test multiple Python versions
- **Coverage Service Integration**: Upload to Codecov or similar
- **Performance Testing**: Add performance benchmarks
- **Deployment**: Add deployment job for releases
- **Notifications**: Slack/email notifications on failures

### Configuration Options

- Adjust Python version requirements
- Add additional quality checks
- Configure coverage thresholds
- Set up branch protection rules

## Related Documentation

- **[TESTING.md](./TESTING.md)**: Comprehensive test suite documentation
- **[LINTING_FORMATTING_STATUS.md](./LINTING_FORMATTING_STATUS.md)**: Code quality standards
- **[README.md](../README.md)**: Project overview and quick start

---

**Last Updated**: 2025-01-15
