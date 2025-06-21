#!/bin/bash

# HustleBuddy Docker Setup Script
echo "🚀 Starting HustleBuddy..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please copy .env.template to .env and add your OpenAI API key:"
    echo "   cp .env.template .env"
    echo "   Then edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Check if OPENAI_API_KEY is set in .env
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Warning: Please make sure your OPENAI_API_KEY is set in .env file"
    echo "📝 Edit .env and replace 'your_openai_api_key_here' with your actual OpenAI API key"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Stop any running containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Build and start all services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ HustleBuddy is ready!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo "🗄️  Database: localhost:5432"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart" 