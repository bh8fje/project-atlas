#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

PYTHONPATH="$project_root/src" python3 -m project_atlas.local_service &
service_pid=$!

cleanup() {
  kill "$service_pid" 2>/dev/null || true
}

trap cleanup EXIT INT TERM
npm --prefix "$project_root/dashboard" run dev
