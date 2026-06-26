set windows-shell := ["powershell"]

# default command lists all available recipes
[default]
_default:
    @just --list --unsorted

import? "init.just"

alias c := clean
alias d := docs
alias h := hooks
alias i := info
alias l := lint
alias q := check
alias t := test
alias hi := hooks-install
alias ty := types
alias fmt := format

# display the system/project information
info:
    @echo "Architecture: {{ arch() }}"
    @echo "Operating Sys: {{ os_family() }}, {{ os() }}"
    @echo "Number of CPU: {{ num_cpus() }}"
    @echo "Project: `uv version`"

# setup the virtualenv
venv *args:
    uv sync --all-extras {{ args }}

# setup virtualenv and install pre-commit hooks
dev: venv hooks-install

# run the formatter
format:
    uv run ruff format .

# run the linter [arg:<full|concise|...>]
lint arg="concise":
    uv run ruff check . --fix --output-format={{ arg }}

# run the type checker [arg:<full|concise|...>]
types arg="concise":
    uv run ty check --output-format={{ arg }}

# lint, format and type-check [arg:<full|concise|...>]
check arg="concise":
    -@just format
    -@just lint {{ arg }}
    -@just types {{ arg }}

# run the tests across all packages (useful flags: -v, --pdb, -k)
test *args:
    uv run pytest packages/ {{ args }}

# run the tests in different Python versions
testall *args:
    uv run --python=3.12 pytest packages/ {{ args }}
    uv run --python=3.14 pytest packages/ {{ args }}

# inspect the test coverage in a browser
cover:
    uv run pytest --cov-report=html packages/
    uv run python -m webbrowser htmlcov/index.html

# run the formatter, linter, typechecker and the tests
ci python="3.12":
    uv run --python={{ python }} ruff format .
    uv run --python={{ python }} ruff check . --fix
    uv run --python={{ python }} ty check .
    uv run --python={{ python }} pytest packages/

# install the pre-commit hooks
hooks-install:
    uvx prek install

# run the pre-commit hooks
hooks:
    uvx prek run --all-files

# clean all build/compilation and cache files and directories
clean:
    rm -fr .cache/
    rm -fr .coverage
    rm -fr .pytest_cache/
    rm -fr .ruff_cache/
    rm -fr .venv/
    rm -fr build/
    rm -fr dist/
    rm -fr init.just
    rm -fr site/
    find . -name '*.egg' -exec rm -f {} +
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '.DS_Store' -exec rm -fr {} +
    find . -name '__pycache__' -exec rm -fr {} +


# serve the documentation on localhost [port:9000]
docs port="9000":
    uv run zensical serve --dev-addr localhost:{{ port }}

_ensure_clean:
    @git diff --quiet
    @git diff --cached --quiet

_set_version target:
    case "{{ target }}" in \
        [0-9]*.[0-9]*.[0-9]*) \
            uv version {{ target }} ;; \
        *) \
            uv version --bump {{ target }} ;; \
    esac
    uv lock

# write the changelog from commit messages (https://git-cliff.org/)
changelog *args:
    uvx git-cliff -o {{ args }}

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock CHANGELOG.md packages/
    git commit -m "chore(release): bump version to {{ version }}"
    git tag -a "v{{ version }}"

# make a new release [target:<major|minor|patch|...> or semver]
release target: ci
    @just _ensure_clean
    @just _set_version {{ target }}
    @just changelog --tag `uv version --short`
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
