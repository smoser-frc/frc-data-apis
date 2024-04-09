#!/bin/sh
fail() { echo "$@" 1>&2; exit 1; }
vrun() { echo "$" "$@" 1>&2; "$@"; }

vrun python3 -m venv ./venv || fail "failed setting up venv"
vrun ./venv/bin/pip install --requirement=requirements.txt ||
    fail "failed installing requirements"

cat <<EOF
Set up ~/.frc-apis.json like this:
{
  "auth": {
    "tba": {"key": "abcdefgHIJKLMNOPQRStuvwxyx0123456789abcdefgjijklmnopqrstuvwxyzab"},
    "frc": {"user": "youruser", "key": "abcdef00-dead-beef-0000-abcdef012345"}
  }
}
EOF
