#!/bin/bash

# Quick fix script to restart Streamlit with correct settings

echo "🔄 Restarting Streamlit with updated configuration..."

# Kill any running Streamlit processes
pkill -f "streamlit run app.py" 2>/dev/null

echo "✅ Stopped old Streamlit process"

# Wait a moment
sleep 2

# Start Streamlit with the app
echo "🚀 Starting Streamlit..."
streamlit run app.py
