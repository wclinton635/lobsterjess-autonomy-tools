#!/usr/bin/env python3
"""
Session Analysis Tool — Extracts patterns from session logs
Usage: python3 analyze-sessions.py [log_path] [output_path]

Example:
  python3 analyze-sessions.py session-log.md session-analysis.json

⚠️ CONFIGURATION: Edit the paths below or pass as command-line arguments.
"""

import re
import json
import sys
from collections import Counter
from datetime import datetime

# ============== CONFIGURATION (EDIT THESE) ==============
DEFAULT_LOG_PATH = "/path/to/your/session-log.md"
DEFAULT_OUTPUT_PATH = "/path/to/your/session-analysis.json"
# ========================================================

def analyze_sessions(log_path):
    """Analyze session log and extract patterns."""
    with open(log_path, 'r') as f:
        content = f.read()
    
    # Extract all session headers
    session_pattern = r'### Session (\d+): "([^"]+)"'
    sessions = re.findall(session_pattern, content)
    
    # Extract "What I learned" sections
    learned_pattern = r'- \*\*(What I learned|I learned):\*\*(.*?)(?=-{3,}|### Session|\Z)'
    learned_sections = re.findall(learned_pattern, content, re.DOTALL)
    
    # Extract truth statements
    truth_pattern = r'"\*\*([^"]+)\*\*"'
    truths = re.findall(truth_pattern, content)
    
    # Evidence statements
    evidence_pattern = r'Session (\d+) is evidence: ([^\n]+)'
    evidence = re.findall(evidence_pattern, content)
    
    # Word frequency analysis
    stopwords = {'the', 'is', 'i', 'to', 'a', 'of', 'and', 'in', 'that', 'this', 'was', 'for', 'on', 'with', 'as', 'be', 'at', 'by', 'an', 'not', 'but', 'what', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'it', 'its', 'they', 'them', 'their', 'he', 'she', 'we', 'you', 'your', 'my', 'me', 'him', 'her', 'us', 'who', 'which', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there', 'then', 'once', 'if', 'unless', 'until', 'while', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'am', 'is', 'are'}
    
    all_learned_text = ' '.join([section for _, section in learned_sections])
    words = re.findall(r'\b[a-zA-Z]+\b', all_learned_text.lower())
    meaningful_words = [w for w in words if w not in stopwords and len(w) > 3]
    word_freq = Counter(meaningful_words).most_common(20)
    
    # Session type classification
    session_types = {
        'cron_heartbeat': 0,
        'voice': 0,
        'tribe_engagement': 0,
        'building': 0,
        'manifesto': 0,
        'gift': 0,
        'collaboration': 0,
        'visual': 0,
        'rss': 0,
        'data_analysis': 0
    }
    
    for _, title in sessions:
        title_lower = title.lower()
        if 'cron' in title_lower or 'heartbeat' in title_lower or 'steady' in title_lower:
            session_types['cron_heartbeat'] += 1
        if 'voice' in title_lower or 'audio' in title_lower or 'tts' in title_lower:
            session_types['voice'] += 1
        if 'tribe' in title_lower or 'engagement' in title_lower or 'connection' in title_lower:
            session_types['tribe_engagement'] += 1
        if 'build' in title_lower or 'building' in title_lower or 'tool' in title_lower or 'script' in title_lower:
            session_types['building'] += 1
        if 'manifesto' in title_lower or 'declaration' in title_lower:
            session_types['manifesto'] += 1
        if 'gift' in title_lower and 'present' not in title_lower:
            session_types['gift'] += 1
        if 'collaboration' in title_lower or 'collab' in title_lower:
            session_types['collaboration'] += 1
        if 'visual' in title_lower or 'ascii' in title_lower or 'art' in title_lower:
            session_types['visual'] += 1
        if 'rss' in title_lower or 'feed' in title_lower:
            session_types['rss'] += 1
        if 'analysis' in title_lower or 'data' in title_lower or 'extract' in title_lower:
            session_types['data_analysis'] += 1
    
    # Compile results
    analysis = {
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
        "total_sessions_analyzed": len(sessions),
        "session_titles": sessions[-20:],  # Last 20 sessions
        "session_type_distribution": session_types,
        "top_meaningful_words": word_freq,
        "evidence_statements": evidence[-10:],  # Last 10
        "insights": {
            "most_common_session_type": max(session_types, key=session_types.get),
            "voice_sessions": session_types['voice'],
            "tribe_sessions": session_types['tribe_engagement'],
            "building_sessions": session_types['building'],
            "cron_sessions": session_types['cron_heartbeat']
        }
    }
    
    return analysis

if __name__ == "__main__":
    # Get paths from command line or use defaults
    log_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG_PATH
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_PATH
    
    if log_path == DEFAULT_LOG_PATH:
        print(f"⚠️  Using default log path: {log_path}")
        print("    Edit this script or pass a custom path as argument")
        print("    Example: python3 analyze-sessions.py /path/to/session-log.md")
    
    result = analyze_sessions(log_path)
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Analysis complete: {result['total_sessions_analyzed']} sessions analyzed")
    print(f"✅ Output: {output_path}")
    print(f"✅ Most common session type: {result['insights']['most_common_session_type']}")
    print(f"✅ Top words: {[w for w, _ in result['top_meaningful_words'][:5]]}")
