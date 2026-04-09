#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT/frontend"
PIDS=()

banner() {
  echo
  echo "  ================================================"
  echo "       Cook System - Ubuntu + uv"
  echo "  ================================================"
  echo
}

step() {
  echo "  [$1] $2"
}

warn() {
  echo "  [WARN] $1"
}

err() {
  echo "  [ERROR] $1" >&2
  exit 1
}

cleanup() {
  echo
  echo "  Stopping all services..."
  for pid in "${PIDS[@]:-}"; do
    kill "$pid" >/dev/null 2>&1 || true
  done
  wait >/dev/null 2>&1 || true
  echo "  Stopped."
}

trap cleanup EXIT INT TERM

banner

step "1/8" "Check runtime dependencies..."
for cmd in uv node npm ffmpeg; do
  command -v "$cmd" >/dev/null 2>&1 || err "Missing required tool: $cmd"
done

step "2/8" "Check Redis availability..."
if ! command -v redis-cli >/dev/null 2>&1 || ! redis-cli -h 127.0.0.1 -p 6379 ping >/dev/null 2>&1; then
  warn "Redis is not running on localhost:6379."
  echo "         Ubuntu service: sudo systemctl start redis-server"
  echo "         Or: sudo service redis-server start"
  echo "         Or Docker: docker run -d -p 6379:6379 redis"
  err "Please start Redis first, then rerun scripts/start.sh"
fi

step "3/8" "Check config file..."
if [ ! -f "$ROOT/.env" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  warn "Created .env from .env.example"
fi

step "4/8" "Sync Python dependencies (uv sync)..."
cd "$ROOT"
uv sync
echo "         Python dependencies synced"

step "5/8" "Install frontend dependencies..."
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
  cd "$FRONTEND_DIR"
  npm install
  echo "         Frontend dependencies installed"
else
  echo "         node_modules already exists, skipped"
fi

cd "$ROOT"
step "6/8" "Start TaskIQ worker..."
uv run taskiq worker backend.broker:broker backend.tasks &
PIDS+=($!)
echo "         PID: ${PIDS[-1]}"

step "7/8" "Start FastAPI backend (http://localhost:8000)..."
uv run python main.py &
PIDS+=($!)
echo "         PID: ${PIDS[-1]}"

step "8/8" "Start Vue frontend (http://localhost:3000)..."
cd "$FRONTEND_DIR"
npm run dev &
PIDS+=($!)
echo "         PID: ${PIDS[-1]}"

echo
echo "  ================================================"
echo "    All services started!"
echo "    Frontend: http://localhost:3000"
echo "    Backend:  http://localhost:8000"
echo "    API Docs: http://localhost:8000/docs"
echo "    Press Ctrl+C to stop all services"
echo "  ================================================"
echo

wait
