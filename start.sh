#!/bin/bash

# 🚀 Complete Startup Guide for Endee RAG System

echo "════════════════════════════════════════════════════════════"
echo "  🚀 Starting Endee RAG System"
echo "════════════════════════════════════════════════════════════"
echo ""

# Step 1: Start Endee Vector Database
echo "📦 Step 1: Starting Endee Vector Database..."
echo "Command: docker compose up -d"
echo ""

docker compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Endee started successfully!"
else
    echo "❌ Failed to start Endee. Make sure Docker is running."
    exit 1
fi

echo ""
echo "⏳ Waiting for Endee to be ready (5 seconds)..."
sleep 5

# Step 2: Check if Endee is running
echo ""
echo "🔍 Step 2: Checking Endee status..."
if docker ps | grep -q endee-server; then
    echo "✅ Endee is running on port 8080"
else
    echo "❌ Endee is not running. Check logs with: docker logs endee-server"
    exit 1
fi

# Step 3: Install/Update dependencies
echo ""
echo "📚 Step 3: Installing Python dependencies..."
echo "Command: pip install -r requirements.txt"
echo ""

pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Step 4: Ready to run Streamlit
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ Setup Complete! Ready to launch Streamlit"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🎯 To start the Streamlit app, run:"
echo ""
echo "   streamlit run app.py"
echo ""
echo "The app will open in your browser at: http://localhost:8501"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📝 Quick Tips:"
echo "  • Your Groq API key is already configured in .env ✅"
echo "  • Upload documents in the sidebar"
echo "  • Click 'Index Documents' to process them"
echo "  • Ask questions in the main interface"
echo ""
echo "🛑 To stop Endee later: docker compose down"
echo "📊 To view Endee logs: docker logs endee-server"
echo ""
