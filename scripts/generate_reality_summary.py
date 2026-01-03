#!/usr/bin/env python3
"""
Generate GitHub Actions Summary for Reality Check
Used by .github/workflows/reality-check.yml
"""

import json
import os
import sys
import glob
from pathlib import Path


def main():
    """Generate GitHub Actions summary from Reality Check results"""
    
    # Find latest JSON report
    report_files = glob.glob('data/reality_checks/*.json')
    if not report_files:
        print("No report files found")
        return
    
    latest_file = max(report_files, key=os.path.getmtime)
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # Get summary file path from environment
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY', '')
    if not summary_path:
        print("GITHUB_STEP_SUMMARY not set, writing to stdout")
        # Use sys.stdout for cross-platform compatibility
        summary = sys.stdout
    else:
        summary = open(summary_path, 'a')
    
    try:
        # Header
        summary.write("# 🥽 Reality Check Report\n\n")
        summary.write(f"**Timestamp:** {data['timestamp']}\n")
        summary.write(f"**Overall Status:** {data['overall_status']}\n\n")
        summary.write("---\n\n")
        summary.write("## 📋 Check Results\n\n")
        
        # Individual checks
        for check in data['checks']:
            status_emoji = {
                'OK': '✅',
                'WARNING': '⚠️',
                'CRITICAL': '🚨',
                'ERROR': '❌'
            }
            emoji = status_emoji.get(check['status'], '❓')
            
            summary.write(f"### {emoji} {check['name']}\n\n")
            summary.write(f"**Status:** {check['status']}  \n")
            summary.write(f"**Confidence:** {check['confidence']:.0%}  \n")
            summary.write(f"**Message:** {check['message']}\n\n")
            
            # Add key details for Bug Scan
            if check['name'] == 'Bug Scan' and 'summary' in check['details']:
                summary.write("**Issues Found:**\n")
                for key, value in check['details']['summary'].items():
                    if value > 0:
                        summary.write(f"- {key.replace('_', ' ').title()}: {value}\n")
                summary.write("\n")
            
            summary.write("---\n\n")
        
        # Philosophy
        summary.write("## 🥽 Reality Glasses Philosophy\n\n")
        summary.write("- ✅ **PROACTIVE** - Scanned before problems reported\n")
        summary.write("- ✅ **VERIFY** - Checked facts, didn't guess\n")
        summary.write("- ✅ **TRUTH** - Measured reality with confidence scores\n")
        summary.write("- ✅ **REALITY** - Used sensors, not assumptions\n\n")
        
        summary.write(f"📄 **Report:** `{Path(latest_file).name}`\n")
    
    finally:
        # Close file if we opened it (not stdout)
        if summary_path:
            summary.close()
    
    print(f"Summary generated from: {latest_file}")


if __name__ == "__main__":
    main()
