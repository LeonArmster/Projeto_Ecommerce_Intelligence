# Local Code Quality Checks

This project uses a small, opt-in set of local checks. These complement the existing pytest GitHub Actions workflow; they are not a substitute for database/dbt/Airflow validation.

## Prerequisites

From the repository root, with Python 3.12 and uv installed:

```bash
uv sync --locked --group dev
```

## Ruff

```bash
uv run --no-sync ruff check src tests airflow/dags
```

The initial rule set is configured in `ruff.toml` and focuses on common Python errors. Ruff does not automatically modify files. For a targeted check, pass the modified Python file path instead of the entire source tree.

## Pre-commit

Install the pre-commit CLI as an isolated uv tool and register the Git hook:

```bash
uv tool install pre-commit
uv tool run pre-commit install
```

After installation, hooks run automatically for staged files on `git commit`. Run them manually:

```bash
uv tool run pre-commit run
```

To inspect all tracked files (this may reveal pre-existing formatting issues):

```bash
uv tool run pre-commit run --all-files
```

Hooks check trailing whitespace, final newline, YAML syntax, merge-conflict markers, and Python Ruff rules. The YAML hook uses `--unsafe` to accept custom YAML tags; it does not validate application-specific dbt or Docker configuration.

**Scope note:** The first PR adds configuration only. It does not mass-reformat or fix legacy Python files. If a repository-wide run reveals existing issues, handle them in a separate scoped change rather than bundling them into the configuration PR.

## Existing test suite

```bash
uv run --no-sync pytest tests/ -v
```

GitHub Actions runs pytest on pull requests into `main`. The new pre-commit checks are local until a separate CI change is approved.

## Related documentation

- [Engineering conventions](../AGENTS.md)
- [Project setup](setup.md)
- [dbt modeling and quality](dbt.md)
