# Codet

[![PyPI version](https://badge.fury.io/py/codet.svg)](https://pypi.org/project/codet/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/clemente0731/codet/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/clemente0731/codet/actions)

A cross-platform command-line tool for Git repository analysis. Profile commit history, detect code hotspots, generate diff reports, and optionally leverage AI for deeper insights. The generated git diff files integrate seamlessly with Cursor for collaborative development.

## Features

- **Commit history analysis** - browse and filter recent commits by time range, author, email, keyword, or commit hash
- **Code hotspot detection** - identify frequently modified files and directories to spot active areas
- **Flexible search modes** - union (match any condition) or intersection (match all conditions)
- **Diff report generation** - produce aggregated `.diff` report files for review in Cursor or other tools
- **AI-powered analysis** - optional OpenAI / Azure OpenAI integration for automated commit summarization
- **Interactive dashboard** - Plotly Dash visualization via the `codet-dash` command
- **JSON export** - structured per-commit JSON output for downstream pipelines (`-oj`)
- **Cross-platform** - works on Windows, macOS, and Linux

## Installation

### From PyPI

```bash
pip install codet
```

### From source

```bash
git clone https://github.com/clemente0731/codet.git
cd codet
pip install -e .
```

### Development dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

```bash
# analyze the current repo, last 7 days, with hotspot analysis
codet -d 7 -s

# search for keywords "Triton" and "cuda" in a cloned repo
git clone https://github.com/pytorch/pytorch.git
codet -d 7 -k Triton -k cuda -s -p pytorch

# filter by author email
codet -d 14 -e alice@example.com

# filter by commit hash (supports partial match)
codet -c abc1234

# intersection mode: must match ALL conditions
codet -d 7 -k feature -e dev@example.com -m intersection
```

## CLI Reference

```
usage: codet [-h] [--version] [-d DAYS] [-e EMAIL] [-u USER] [-k KEYWORD]
             [-c COMMIT] [-g] [-r] [-p PATH] [-s] [-m {union,intersection}]
             [-mo MODEL] [-to API_TOKEN] [-oe OPENAI_ENDPOINT]
             [-cp CUSTOM_PROMPT] [-f INPUT_FILE] [-oj]
```

### Basic Options

| Flag | Description | Default |
|------|-------------|---------|
| `-d`, `--days` | Look back N days for commits | `30` |
| `-e`, `--email` | Filter by author email (repeatable) | — |
| `-u`, `--user` | Filter by author name (repeatable) | — |
| `-k`, `--keyword` | Search keyword in commit diffs (repeatable) | — |
| `-c`, `--commit` | Filter by commit hash, supports partial match (repeatable) | — |
| `-g`, `--debug` | Enable debug logging | `False` |
| `-r`, `--recursive` | Recursively scan subdirectories for git repos | `True` |
| `-p`, `--path` | Path to analyze | current directory |
| `-s`, `--hotspot` | Enable code hotspot analysis | `True` |
| `-m`, `--mode` | Search mode: `union` or `intersection` | `union` |

### AI Options

| Flag | Description | Default |
|------|-------------|---------|
| `-mo`, `--model` | OpenAI model name | `gpt-4.1-20250414` |
| `-to`, `--api-token` | API token (or set `AI_API_TOKEN` env var) | — |
| `-oe`, `--openai-endpoint` | Azure OpenAI endpoint URL | — |
| `-cp`, `--custom-prompt` | Custom prompt appended to AI analysis | — |
| `-f`, `--input-file` | Additional file to include in AI analysis | — |
| `-oj`, `--output-cook-json` | Export per-commit JSON reports to `json_cook/` | `False` |

## Dashboard

Codet includes an interactive Plotly Dash dashboard for visualizing analysis results.

```bash
# launch dashboard with JSON data directory
codet-dash --json-path json_cook/
```

## Output

### Diff Report

Each run generates a `git_patch_report_<timestamp>.diff` file containing aggregated patches with contextual metadata. Open it directly in Cursor for AI-assisted code review.

### JSON Export

With `-oj`, per-commit JSON files are written to `json_cook/<repo_name>/`, each containing commit metadata, changed files, and optional AI summaries.

## Development

```bash
git clone https://github.com/clemente0731/codet.git
cd codet
pip install -e ".[dev]"

# lint
flake8 . --max-line-length=127

# format
black .
isort .

# test
pytest
```

## License

MIT License. See [LICENSE](LICENSE) for details.
