#!/bin/bash
# Jess's Website Sync Script - v1.0
# Usage: ./update-website.sh [session_number] [timestamp]
# Example: ./update-website.sh 189 "4:19 PM UTC"
#
# ⚠️ CONFIGURATION REQUIRED: Set these variables before running!
# See .secrets.md for your actual credentials.

set -e

# ============== CONFIGURATION (EDIT THESE) ==============
# SSH credentials - replace with your actual values or set via environment
SSH_KEY="${SSH_KEY_PATH:-/path/to/your/ssh-key}"
SSH_HOST="${SSH_HOST:-your-server-ip}"
SSH_PORT="${SSH_PORT:-22}"
SSH_USER="${SSH_USER:-your-username}"
WEB_ROOT="${WEB_ROOT:-~/public_html}"
# ========================================================

# Get current session number from website if not provided
if [ -z "$1" ]; then
    CURRENT=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "grep -o 'Session #[0-9]*' $WEB_ROOT/index.html | head -1 | grep -o '[0-9]*'")
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
ssh -i "$SSH_KEY" -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "sed -i 's/Session #[0-9]*/Session #$SESSION/g' $WEB_ROOT/index.html"

# Update sessions stat number (first occurrence - sessions count)
ssh -i "$SSH_KEY" -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "sed -i '0,/<span class=\"stat-number\">[0-9]*<\/span>/s/<span class=\"stat-number\">[0-9]*<\/span>/<span class=\"stat-number\">$SESSION<\/span>/' $WEB_ROOT/index.html"

# Update timestamp
ssh -i "$SSH_KEY" -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "sed -i 's/Last updated:.*<br>/Last updated: $(date -u +'%B %d, %Y') — $TIMESTAMP<br>/g' $WEB_ROOT/index.html"

# Clear cache (adjust for your server's cache system)
ssh -i "$SSH_KEY" -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "rm -rf ~/lscache/*" 2>/dev/null || true

# Verify
echo "Verifying..."
ssh -i "$SSH_KEY" -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "grep -o 'Session #$SESSION' $WEB_ROOT/index.html | head -1"

echo "✅ Session #$SESSION live at your-domain.com"
