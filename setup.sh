#!/bin/bash

# Setup script for Endee RAG System

echo "🚀 Setting up Endee RAG System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it and add your OpenAI API key."
else
    echo "✅ .env file already exists"
fi

# Start Endee vector database
echo "🐳 Starting Endee vector database..."
docker compose up -d

# Wait for Endee to be ready
echo "⏳ Waiting for Endee to be ready..."
sleep 5

# Check if Endee is running
if docker ps | grep -q endee-server; then
    echo "✅ Endee is running on port 8080"
else
    echo "❌ Endee failed to start. Check logs with: docker logs endee-server"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Run the application: streamlit run app.py"
echo "3. Upload documents and start asking questions!"
echo ""
echo "To stop Endee: docker compose down"
echo "To view Endee logs: docker logs endee-server"
