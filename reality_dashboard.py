#!/usr/bin/env python3
"""
🥽 UMAJA Reality Analyzer Dashboard
Interactive Streamlit dashboard for visualizing Reality Agent checks
"""

import streamlit as st
import json
import glob
import os
from pathlib import Path
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="🥽 UMAJA Reality Analyzer",
    page_icon="🥽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .status-ok {
        color: #00ff88;
    }
    .status-warning {
        color: #ffaa00;
    }
    .status-critical {
        color: #ff0044;
    }
</style>
""", unsafe_allow_html=True)

def load_latest_report():
    """Load the latest reality check report"""
    reports_dir = Path('data/reality_checks')
    
    if not reports_dir.exists():
        return None
    
    json_files = list(reports_dir.glob('*.json'))
    
    if not json_files:
        return None
    
    # Get the most recent file
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    
    with open(latest_file, 'r') as f:
        return json.load(f)

def get_status_emoji(status):
    """Get emoji for status"""
    status_map = {
        'OK': '✅',
        'WARNING': '⚠️',
        'CRITICAL': '🚨',
        'ERROR': '❌',
        'HEALTHY': '✅'
    }
    return status_map.get(status.upper(), '❓')

def get_status_color(status):
    """Get color class for status"""
    if status.upper() in ['OK', 'HEALTHY']:
        return 'status-ok'
    elif status.upper() == 'WARNING':
        return 'status-warning'
    else:
        return 'status-critical'

# Title
st.title("🥽 UMAJA Reality Analyzer")
st.markdown("**Real-time Reality Agent Monitoring Dashboard**")
st.markdown("---")

# Auto-refresh toggle
col1, col2 = st.columns([3, 1])
with col2:
    auto_refresh = st.checkbox("Auto-refresh (10s)", value=True)

# Load data
data = load_latest_report()

if data is None:
    st.error("⚠️ No reality check data found. Please run the Reality Agent first.")
    st.code("python src/reality_agent.py")
    st.stop()

# Overall metrics in columns
st.subheader("📊 Overall Status")
col1, col2, col3, col4 = st.columns(4)

with col1:
    overall_status = data.get('overall_status', 'UNKNOWN')
    st.metric(
        label="System Status",
        value=overall_status,
        delta=None
    )
    st.markdown(f"<h1 style='text-align: center;'>{get_status_emoji(overall_status)}</h1>", 
                unsafe_allow_html=True)

with col2:
    checks = data.get('checks', [])
    total_checks = len(checks)
    passed_checks = len([c for c in checks if c['status'] == 'OK'])
    st.metric(
        label="Checks Passed",
        value=f"{passed_checks} / {total_checks}",
        delta=None
    )

with col3:
    if total_checks > 0:
        success_rate = (passed_checks / total_checks) * 100
    else:
        success_rate = 0
    st.metric(
        label="Success Rate",
        value=f"{success_rate:.1f}%",
        delta=None
    )

with col4:
    if total_checks > 0:
        avg_confidence = sum(c['confidence'] for c in checks) / total_checks * 100
    else:
        avg_confidence = 0
    st.metric(
        label="Avg Confidence",
        value=f"{avg_confidence:.1f}%",
        delta=None
    )

st.markdown("---")

# Last update time
timestamp = data.get('timestamp', '')
if timestamp:
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        st.caption(f"🕐 Last updated: {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    except:
        st.caption(f"🕐 Last updated: {timestamp}")

st.markdown("---")

# Individual checks
st.subheader("🔍 Reality Checks")

for check in checks:
    status = check.get('status', 'UNKNOWN')
    name = check.get('name', 'Unknown Check')
    message = check.get('message', '')
    confidence = check.get('confidence', 0) * 100
    details = check.get('details', {})
    
    with st.expander(f"{get_status_emoji(status)} {name} - {status}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Message:** {message}")
            st.progress(confidence / 100)
            st.caption(f"Confidence: {confidence:.1f}%")
        
        with col2:
            st.markdown(f"**Status:** `{status}`")
            check_time = check.get('timestamp', '')
            if check_time:
                try:
                    ct = datetime.fromisoformat(check_time.replace('Z', '+00:00'))
                    st.caption(f"Time: {ct.strftime('%H:%M:%S')}")
                except:
                    st.caption(f"Time: {check_time}")
        
        # Show details
        if details:
            st.markdown("**Details:**")
            
            # Special formatting for Bug Scan
            if name == "Bug Scan" and 'summary' in details:
                summary = details['summary']
                cols = st.columns(4)
                metrics = [
                    ("Naive DateTime", summary.get('naive_datetime', 0)),
                    ("TODOs", summary.get('todos', 0)),
                    ("Missing Handlers", summary.get('missing_error_handling', 0)),
                    ("Credentials", summary.get('hardcoded_credentials', 0))
                ]
                for col, (label, value) in zip(cols, metrics):
                    col.metric(label, value)
            else:
                st.json(details)

st.markdown("---")

# Raw data viewer
with st.expander("📄 Raw JSON Data"):
    st.json(data)

st.markdown("---")

# Charts
st.subheader("📈 Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Confidence Scores**")
    
    # Prepare data for chart
    chart_data = {
        'Check': [c['name'] for c in checks],
        'Confidence': [c['confidence'] * 100 for c in checks]
    }
    st.bar_chart(chart_data, x='Check', y='Confidence', height=300)

with col2:
    st.markdown("**Status Distribution**")
    
    # Count statuses
    status_counts = {}
    for check in checks:
        status = check['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Display as metrics
    for status, count in status_counts.items():
        st.metric(
            label=f"{get_status_emoji(status)} {status}",
            value=count
        )

st.markdown("---")

# Philosophy footer
st.markdown("""
### 🥽 Reality Glasses Philosophy

- ✅ **PROACTIVE** - Scanned before problems reported
- ✅ **VERIFY** - Checked facts, didn't guess  
- ✅ **TRUTH** - Measured reality with confidence scores
- ✅ **REALITY** - Used sensors, not assumptions

*Serving Truth with Humility* 🥽✨
""")

# Auto-refresh
if auto_refresh:
    time.sleep(10)
    st.rerun()
