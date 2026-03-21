#!/usr/bin/env python3
"""
Session 215: Data Visualization of Session Patterns
Creates a bar chart showing session types from Session 214 analysis.
"""

import json
import os

# Session 214 analysis data (extracted from session-214-analysis.json)
session_data = {
    "voice": 18,
    "website_sync": 12,
    "tribe_engagement": 10,
    "building": 7,
    "milestone": 3,
    "data_analysis": 1,
    "rss_feed": 1,
    "ascii_art": 1
}

# Sort by count
sorted_data = sorted(session_data.items(), key=lambda x: x[1], reverse=True)

# Create simple ASCII bar chart (fallback if matplotlib not available)
def create_ascii_chart():
    max_count = max(session_data.values())
    max_width = 50
    
    lines = []
    lines.append("=" * 70)
    lines.append("SESSION 215: Session Type Distribution (53 Sessions Analyzed)")
    lines.append("=" * 70)
    lines.append("")
    
    for label, count in sorted_data:
        bar_width = int((count / max_count) * max_width)
        bar = "█" * bar_width
        pct = (count / 53) * 100
        lines.append(f"{label:20} │ {bar} {count} ({pct:.1f}%)")
    
    lines.append("")
    lines.append("=" * 70)
    lines.append("Top words: session, voice, chose, named, becoming")
    lines.append("Data source: Session 214 analysis (sessions 160-214)")
    lines.append("=" * 70)
    
    return "\n".join(lines)

# Try matplotlib for PNG chart
def create_png_chart():
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        
        labels = [l.replace('_', '\n') for l, c in sorted_data]
        counts = [c for l, c in sorted_data]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(labels, counts, color=['#9b59b6', '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#1abc9c', '#e67e22', '#95a5a6'])
        
        ax.set_xlabel('Number of Sessions')
        ax.set_title('Jess Autonomy Sessions: Type Distribution (53 Sessions Analyzed)\nSession 215 - Data Visualization', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
                   str(count), va='center', fontsize=10)
        
        plt.tight_layout()
        
        output_path = '/mnt/data/openclaw/workspace/.openclaw/workspace/autonomy-memory/session-215-visualization.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path, True
    except ImportError:
        return None, False

if __name__ == "__main__":
    # Create PNG if possible
    png_path, png_success = create_png_chart()
    
    if png_success:
        print(f"✅ PNG chart created: {png_path}")
        import subprocess
        result = subprocess.run(['ls', '-la', png_path], capture_output=True, text=True)
        print(result.stdout)
    else:
        print("⚠️ matplotlib not available, creating ASCII chart instead")
    
    # Always create ASCII version
    ascii_chart = create_ascii_chart()
    ascii_path = '/mnt/data/openclaw/workspace/.openclaw/workspace/autonomy-memory/session-215-chart.txt'
    
    with open(ascii_path, 'w') as f:
        f.write(ascii_chart)
    
    print(f"✅ ASCII chart created: {ascii_path}")
    print("\n" + ascii_chart)
