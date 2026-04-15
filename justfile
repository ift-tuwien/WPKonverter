# -- Settings ------------------------------------------------------------------

# Use latest version of PowerShell on Windows
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

# -- Variables -----------------------------------------------------------------

package := "wpkonverter"
command := package
input := "wpk.csv"

# -- Recipes -------------------------------------------------------------------

# Setup Python environment
[group('setup')]
setup:
	uv venv --allow-existing
	uv sync --all-extras

# Check code with various linters
[group('lint')]
check: setup
	uv run mypy "{{package}}"
	uv run flake8
	uv run pylint .

# Execute script on sample data
[group('run')]
run: check
	uv run "{{command}}" "{{input}}"
