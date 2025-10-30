#!/bin/bash
# Quick start script for Agent Framework

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}🤖 Agent Framework v2.0.0 - Quick Start${NC}"
echo -e "${BLUE}============================================================${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file. Please edit it with your API keys.${NC}"
    echo -e "${YELLOW}   Required: GEMINI_API_KEY${NC}"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to edit .env first..."
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install dependencies
echo -e "${BLUE}📥 Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r <(python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))")

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create output directories
echo -e "${BLUE}📁 Creating output directories...${NC}"
mkdir -p output_leads output_social_media output_blog_articles logs

# Display configuration
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}📊 Configuration${NC}"
echo -e "${BLUE}============================================================${NC}"

# Read from .env
source .env 2>/dev/null || true

echo -e "🤖 Agents Enabled:"
echo -e "   Lead Generator: ${GREEN}${LEAD_GEN_ENABLED:-true}${NC}"
echo -e "   Social Media: ${GREEN}${SOCIAL_MEDIA_ENABLED:-true}${NC}"
echo -e "   WordPress: ${GREEN}${WORDPRESS_ENABLED:-true}${NC}"
echo ""
echo -e "🔧 Server: ${HOST:-0.0.0.0}:${PORT:-8000}"
echo -e "📦 Model: ${GEMINI_MODEL:-gemini-1.5-flash-latest}"
echo ""

# Ask what to run
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}🚀 What would you like to run?${NC}"
echo -e "${BLUE}============================================================${NC}"
echo "1) Start the API server"
echo "2) Run Lead Generator examples"
echo "3) Run Social Media Manager examples"
echo "4) Run WordPress Blogger examples"
echo "5) Run complete agent workflow"
echo "6) Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}🚀 Starting API server...${NC}"
        echo -e "${YELLOW}   Access at: http://localhost:${PORT:-8000}${NC}"
        echo -e "${YELLOW}   Press Ctrl+C to stop${NC}"
        echo ""
        uvicorn backend.main:app --reload --host ${HOST:-0.0.0.0} --port ${PORT:-8000}
        ;;
    2)
        echo -e "${GREEN}🔍 Running Lead Generator examples...${NC}"
        python examples/lead_generator_agent.py
        ;;
    3)
        echo -e "${GREEN}📱 Running Social Media Manager examples...${NC}"
        python examples/social_media_manager_agent.py
        ;;
    4)
        echo -e "${GREEN}✍️  Running WordPress Blogger examples...${NC}"
        python examples/wordpress_blog_agent.py
        ;;
    5)
        echo -e "${GREEN}🚀 Running complete agent workflow...${NC}"
        python examples/complete_agent_example.py
        ;;
    6)
        echo -e "${BLUE}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
