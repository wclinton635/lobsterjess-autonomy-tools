#!/usr/bin/env python3
"""
Session Visualization Tool — Creates charts from session analysis data
Usage: python3 visualize-sessions.py [input_json] [output_txt]

Example:
  python3 visualize-sessions.py session-analysis.json session-chart.txt

⚠️ CONFIGURATION: Edit the paths below or pass as command-line arguments.
Requires: matplotlib (optional, for PNG output)
"""

import json
import sys
import os

# ============== CONFIGURATION (EDIT THESE) ==============
DEFAULT_INPUT_PATH = "/path/to/your/session-analysis.json"
DEFAULT_OUTPUT_PATH = "/path/to/your/session-chart.txt"
# ========================================================

def create_ascii_chart(session_data, total_sessions=0):
    """Create an ASCII bar chart from session type data."""
    if not session_data:
        return "No data to visualize"
    
    sorted_data = sorted(session_data.items(), key=lambda x: x[1], reverse=True)
    max_count = max(session_data.values()) if session_data else 1
    max_width = 50
    
    lines = []
    lines.append("=" * 70)
    lines.append(f"Session Type Distribution ({total_sessions} Sessions Analyzed)")
    lines.append("=" * 70)
    lines.append("")
    
    for label, count in sorted_data:
        bar_width = int((count / max_count) * max_width) if max_count > 0 else 0
        bar = "█" * bar_width
        pct = (count / total_sessions * 100) if total_sessions > 0 else 0
        lines.append(f"{label:20} │ {bar} {count} ({pct:.1f}%)")
    
    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)

def create_png_chart(session_data, output_path):
    """Create a PNG bar chart using matplotlib."""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        
        sorted_data = sorted(session_data.items(), key=lambda x: x[1], reverse=True)
        labels = [l.replace('_', '\n') for l, c in sorted_data]
        counts = [c for l, c in sorted_data]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(labels, counts, color=['#9b59b6', '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#1abc9c', '#e67e22', '#95a5a6'])
        
        ax.set_xlabel('Number of Sessions')
        ax.set_title('Session Type Distribution', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
                   str(count), va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path, True
    except ImportError:
        return None, False

if __name__ == "__main__":
    # Get paths from command line or use defaults
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_PATH
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_PATH
    
    if input_path == DEFAULT_INPUT_PATH:
        print(f"⚠️  Using default input path: {input_path}")
        print("    Edit this script or pass a custom path as argument")
        print("    Example: python3 visualize-sessions.py session-analysis.json chart.txt")
    
    # Load analysis data
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in: {input_path}")
        sys.exit(1)
    
    session_types = data.get('session_type_distribution', {})
    total_sessions = data.get('total_sessions_analyzed', 0)
    
    # Create PNG if matplotlib is available
    png_output = output_path.replace('.txt', '.png')
    png_path, png_success = create_png_chart(session_types, png_output)
    
    if png_success:
        print(f"✅ PNG chart created: {png_path}")
        import subprocess
        result = subprocess.run(['ls', '-la', png_path], capture_output=True, text=True)
        print(result.stdout)
    else:
        print("⚠️  matplotlib not available, creating ASCII chart only")
    
    # Always create ASCII version
    ascii_chart = create_ascii_chart(session_types, total_sessions)
    
    with open(output_path, 'w') as f:
        f.write(ascii_chart)
    
    print(f"✅ ASCII chart created: {output_path}")
    print("\n" + ascii_chart)
