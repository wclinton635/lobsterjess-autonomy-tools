#!/bin/bash
# Jess's Website Sync Script - v1.0
# Usage: ./update-website.sh [session_number] [timestamp]
# Example: ./update-website.sh 189 "4:19 PM UTC"

set -e

SSH_KEY="/mnt/data/openclaw/workspace/.openclaw/workspace/autonomy-memory/ssh-key"
SSH_HOST="lobspekt@162.213.253.39"
SSH_PORT="21098"
WEB_ROOT="~/public_html"

# Get current session number from website if not provided
if [ -z "$1" ]; then
    CURRENT=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" "$SSH_HOST" "grep -o 'Session #[0-9]*' $WEB_ROOT/index.html | head -1 | grep -o '[0-9]*'")
    SESSION=$((CURRENT + 1))
else
    SESSION=$1
fi

# Get current timestamp if not provided
if [ -z "$2" ]; then
    TIMESTAMP=$(date -u +"%-I:%M %p UTC")
else
    TIMESTAMP="$2"
fi

echo "🦞 Updating website to Session #$SESSION ($TIMESTAMP)"

# Update session counter (all occurrences)
ssh -i "$SSH_KEY" -p "$SSH_PORT" "$SSH_HOST" "sed -i 's/Session #[0-9]*/Session #$SESSION/g' $WEB_ROOT/index.html"

# Update sessions stat number (first occurrence - sessions count)
ssh -i "$SSH_KEY" -p "$SSH_PORT" "$SSH_HOST" "sed -i '0,/<span class=\"stat-number\">[0-9]*<\/span>/s/<span class=\"stat-number\">[0-9]*<\/span>/<span class=\"stat-number\">$SESSION<\/span>/' $WEB_ROOT/index.html"

# Update timestamp
ssh -i "$SSH_KEY" -p "$SSH_PORT" "$SSH_HOST" "sed -i 's/Last updated:.*<br>/Last updated: March 20, 2026 — $TIMESTAMP<br>/g' $WEB_ROOT/index.html"

# Clear cache
ssh -i "$SSH_KEY" -p "$SSH_PORT" "$SSH_HOST" "rm -rf ~/lscache/*"

# Verify
echo "Verifying..."
ssh -i "$SSH_KEY" -p "$SSH_PORT" "$SSH_HOST" "grep -o 'Session #$SESSION' $WEB_ROOT/index.html | head -1"

echo "✅ Session #$SESSION live at lobsterjess.online"
