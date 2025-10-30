#!/bin/bash
# Deployment script for Agent Framework

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}🚀 Agent Framework v2.0.0 - Deployment${NC}"
echo -e "${BLUE}============================================================${NC}"

# Check for required files
echo -e "${BLUE}📋 Pre-deployment checks...${NC}"

required_files=(.env pyproject.toml backend/main.py)
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Missing required file: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ All required files present${NC}"

# Check Python version
python_version=$(python3 --version | grep -oP '\d+\.\d+')
if (( $(echo "$python_version < 3.11" | bc -l) )); then
    echo -e "${RED}❌ Python 3.11+ required (found $python_version)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python version: $python_version${NC}"

# Ask deployment type
echo ""
echo -e "${BLUE}🔧 Select deployment type:${NC}"
echo "1) Local Development"
echo "2) Production (Docker)"
echo "3) Production (systemd service)"
echo "4) Cloud (Render/Railway/Heroku)"
echo ""
read -p "Enter your choice (1-4): " deploy_type

case $deploy_type in
    1)
        echo -e "${GREEN}🔧 Setting up Local Development...${NC}"
        
        # Create virtual environment
        if [ ! -d ".venv" ]; then
            python3 -m venv .venv
        fi
        source .venv/bin/activate
        
        # Install dependencies
        pip install -q --upgrade pip
        pip install -e .
        
        # Create directories
        mkdir -p output_leads output_social_media output_blog_articles logs
        
        echo -e "${GREEN}✅ Local development ready!${NC}"
        echo -e "${YELLOW}   Run: ./scripts/run_agent.sh${NC}"
        ;;
        
    2)
        echo -e "${GREEN}🐳 Setting up Docker deployment...${NC}"
        
        # Create Dockerfile
        cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application
COPY . .

# Create output directories
RUN mkdir -p output_leads output_social_media output_blog_articles logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

        # Create docker-compose.yml
        cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  agent-framework:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./output_leads:/app/output_leads
      - ./output_social_media:/app/output_social_media
      - ./output_blog_articles:/app/output_blog_articles
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF

        echo -e "${GREEN}✅ Docker files created!${NC}"
        echo -e "${YELLOW}   Build: docker-compose build${NC}"
        echo -e "${YELLOW}   Run: docker-compose up -d${NC}"
        ;;
        
    3)
        echo -e "${GREEN}🔧 Setting up systemd service...${NC}"
        
        # Get current directory
        current_dir=$(pwd)
        
        # Create systemd service file
        cat > agent-framework.service << EOF
[Unit]
Description=Agent Framework v2.0.0
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$current_dir
Environment="PATH=$current_dir/.venv/bin"
ExecStart=$current_dir/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

        echo -e "${GREEN}✅ Service file created: agent-framework.service${NC}"
        echo -e "${YELLOW}   Install:${NC}"
        echo "   sudo cp agent-framework.service /etc/systemd/system/"
        echo "   sudo systemctl daemon-reload"
        echo "   sudo systemctl enable agent-framework"
        echo "   sudo systemctl start agent-framework"
        ;;
        
    4)
        echo -e "${GREEN}☁️  Setting up Cloud deployment...${NC}"
        
        # Create Procfile for Heroku/Railway
        cat > Procfile << 'EOF'
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
EOF

        # Create runtime.txt
        echo "python-3.11.0" > runtime.txt
        
        # Create render.yaml for Render
        cat > render.yaml << 'EOF'
services:
  - type: web
    name: agent-framework
    env: python
    buildCommand: pip install -e .
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
EOF

        echo -e "${GREEN}✅ Cloud deployment files created!${NC}"
        echo -e "${YELLOW}   Heroku: git push heroku main${NC}"
        echo -e "${YELLOW}   Railway: railway up${NC}"
        echo -e "${YELLOW}   Render: Connect your repo in dashboard${NC}"
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

# Post-deployment instructions
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}✅ Deployment files ready!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "📝 Next Steps:"
echo "   1. Review and update .env with production values"
echo "   2. Set up monitoring and logging"
echo "   3. Configure SSL/TLS certificates"
echo "   4. Set up backup procedures"
echo "   5. Test all endpoints"
echo ""
echo -e "${YELLOW}⚠️  Security Checklist:${NC}"
echo "   [ ] API keys are secure"
echo "   [ ] DEBUG=false in production"
echo "   [ ] CORS configured properly"
echo "   [ ] Rate limiting enabled"
echo "   [ ] Logs are being monitored"
echo ""
