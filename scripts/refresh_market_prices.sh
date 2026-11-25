#!/bin/sh
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ -x "$PROJECT_ROOT/.venv/bin/python" ]; then
  PYTHON="$PROJECT_ROOT/.venv/bin/python"
elif [ -x "$PROJECT_ROOT/venv/bin/python" ]; then
  PYTHON="$PROJECT_ROOT/venv/bin/python"
else
  PYTHON=''
fi

if [ -z "$PYTHON" ]; then
  echo "Python environment not found (.venv or venv) in $PROJECT_ROOT" >&2
  exit 1
fi

cd "$PROJECT_ROOT"
exec "$PYTHON" manage.py import_market_prices --all --limit 100
