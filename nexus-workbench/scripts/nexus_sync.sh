#!/bin/bash
# NEXUS AI-OS — Colab → GitHub Sync Script
# Run from inside the cloned repo: bash nexus-workbench/scripts/nexus_sync.sh
# Requires: git configured with push access, Python 3.x
#
# KANON: _developement (mit 'e') — _development (ohne 'e') ist DELETED
# AP2 Security Gate läuft vor jedem Commit. Bei Exit 1: Abbruch.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORK_DRIVE="/gdrive/My Drive/_developement/LLM-LOCAL-SSOT/WORK"
SCRIPT_DIR="$REPO_ROOT/nexus-workbench/scripts"
SECRET_SCAN="$SCRIPT_DIR/secret_scan.py"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "╔══════════════════════════════════════════════════════╗"
echo "║  NEXUS AI-OS — GitHub Sync                          ║"
echo "║  Repo:   $REPO_ROOT"
echo "║  Branch: $BRANCH"
echo "║  TS:     $TIMESTAMP"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 0. Verify canonical path ─────────────────────────────────────────────────
if echo "$WORK_DRIVE" | grep -q "_development[^e]"; then
    echo "[ERROR] Path contains '_development' without 'e' — VERBOTEN"
    exit 1
fi
echo "[✓] Path check: KANON path with 'e' confirmed"

# ── 1. AP2 Security Gate ──────────────────────────────────────────────────────
echo ""
echo "[AP2] Running secret_scan.py..."
if ! python3 "$SECRET_SCAN" "$REPO_ROOT"; then
    echo "[ERROR] AP2 secret_scan FAILED — secrets detected. Aborting sync."
    exit 1
fi
echo "[✓] AP2 Security Gate: CLEAN"

# ── 2. Pull latest ────────────────────────────────────────────────────────────
echo ""
echo "[GIT] Pulling latest from origin/$BRANCH..."
git fetch origin "$BRANCH" 2>/dev/null || echo "[WARN] Fetch failed — continuing offline"
git merge --ff-only "origin/$BRANCH" 2>/dev/null || echo "[WARN] Already up to date or fast-forward not possible"

# ── 3. Copy Colab outputs from Drive WORK → repo ─────────────────────────────
# Only copy known safe artifact patterns; never copy raw_import_* or *.gz
ARTIFACTS_DIR="$REPO_ROOT/nexus-workbench/artifacts"
mkdir -p "$ARTIFACTS_DIR"

if [ -d "$WORK_DRIVE" ]; then
    echo ""
    echo "[SYNC] Copying artifacts from Drive WORK → $ARTIFACTS_DIR"
    # Golden cases
    for f in "$WORK_DRIVE"/golden_case_*.json; do
        [ -f "$f" ] && cp "$f" "$ARTIFACTS_DIR/" && echo "  ↳ $(basename "$f")"
    done
    # Kernel outputs (timestamped JSON)
    for f in "$WORK_DRIVE"/ec2_*.json "$WORK_DRIVE"/ec5_*.json; do
        [ -f "$f" ] && cp "$f" "$ARTIFACTS_DIR/" && echo "  ↳ $(basename "$f")"
    done
    # WORM ledger snapshot (read-only copy)
    COMMS="$WORK_DRIVE/_COMMS/feedback.jsonl"
    if [ -f "$COMMS" ]; then
        cp "$COMMS" "$ARTIFACTS_DIR/feedback_snapshot_${TIMESTAMP}.jsonl"
        echo "  ↳ feedback.jsonl → feedback_snapshot_${TIMESTAMP}.jsonl"
    fi
    echo "[✓] Drive sync complete"
else
    echo "[WARN] Drive WORK not mounted at $WORK_DRIVE — skipping artifact copy"
    echo "       (Normal in CI — artifacts committed from previous Colab run)"
fi

# ── 4. Stage and commit ───────────────────────────────────────────────────────
echo ""
git add -A
CHANGED=$(git diff --cached --name-only | wc -l)

if [ "$CHANGED" -eq 0 ]; then
    echo "[✓] Nothing to commit — workspace clean"
    exit 0
fi

echo "[GIT] Staging $CHANGED changed file(s):"
git diff --cached --name-only | sed 's/^/  ↳ /'

git commit -m "$(cat <<EOF
sync(nexus): automated Colab → GitHub backup $TIMESTAMP

- Artifacts synced from Drive WORK
- AP2 Security Gate: CLEAN
- Branch: $BRANCH

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01VD5cgBRTaY3Ub6bFfVvDaX
EOF
)"

# ── 5. Push ───────────────────────────────────────────────────────────────────
echo ""
echo "[GIT] Pushing to origin/$BRANCH..."
RETRY=0
MAX_RETRY=4
DELAY=2
while [ $RETRY -lt $MAX_RETRY ]; do
    if git push -u origin "$BRANCH"; then
        echo "[✓] Push successful"
        break
    fi
    RETRY=$((RETRY + 1))
    if [ $RETRY -lt $MAX_RETRY ]; then
        echo "[RETRY $RETRY/$MAX_RETRY] Push failed — waiting ${DELAY}s..."
        sleep $DELAY
        DELAY=$((DELAY * 2))
    else
        echo "[ERROR] Push failed after $MAX_RETRY attempts"
        exit 1
    fi
done

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  [✓] NEXUS Sync COMPLETE — $TIMESTAMP  ║"
echo "╚══════════════════════════════════════════════════════╝"
