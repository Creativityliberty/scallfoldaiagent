#!/bin/bash
# WordPress setup and configuration wizard

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}📝 WordPress Setup Wizard${NC}"
echo -e "${BLUE}============================================================${NC}"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
fi

echo ""
echo -e "${BLUE}This wizard will help you configure WordPress integration.${NC}"
echo ""

# Get WordPress URL
echo -e "${GREEN}Step 1/4: WordPress Site URL${NC}"
read -p "Enter your WordPress site URL (e.g., https://mysite.com): " wp_url

# Validate URL
if [[ ! $wp_url =~ ^https?:// ]]; then
    echo -e "${RED}❌ Invalid URL. Must start with http:// or https://${NC}"
    exit 1
fi

echo -e "${GREEN}✅ WordPress URL: $wp_url${NC}"

# Get WordPress username
echo ""
echo -e "${GREEN}Step 2/4: WordPress Username${NC}"
read -p "Enter your WordPress username: " wp_username

# Get Application Password
echo ""
echo -e "${GREEN}Step 3/4: Application Password${NC}"
echo -e "${YELLOW}📝 To generate an Application Password:${NC}"
echo "   1. Log in to your WordPress admin panel"
echo "   2. Go to Users → Profile"
echo "   3. Scroll to 'Application Passwords'"
echo "   4. Enter 'Agent Framework' as the name"
echo "   5. Click 'Add New Application Password'"
echo "   6. Copy the generated password"
echo ""
read -sp "Enter your Application Password: " wp_password
echo ""

# Test Connection
echo ""
echo -e "${GREEN}Step 4/4: Testing Connection${NC}"
echo -e "${YELLOW}🔍 Testing WordPress API connection...${NC}"

# Test with curl
response=$(curl -s -w "\n%{http_code}" \
    --user "$wp_username:$wp_password" \
    "$wp_url/wp-json/wp/v2/users/me" 2>/dev/null || echo "000")

http_code=$(echo "$response" | tail -n1)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✅ Connection successful!${NC}"
    
    # Extract username from response
    user_data=$(echo "$response" | head -n-1)
    echo -e "${GREEN}   Logged in as: $(echo $user_data | grep -o '"name":"[^"]*"' | cut -d'"' -f4)${NC}"
else
    echo -e "${RED}❌ Connection failed (HTTP $http_code)${NC}"
    echo -e "${YELLOW}   Please check your credentials and try again.${NC}"
    exit 1
fi

# Update .env file
echo ""
echo -e "${BLUE}💾 Saving configuration...${NC}"

# Escape special characters in password
escaped_password=$(printf '%s\n' "$wp_password" | sed 's/[[\.*^$/]/\\&/g')

# Update .env
sed -i.bak "s|WORDPRESS_URL=.*|WORDPRESS_URL=$wp_url|" .env
sed -i.bak "s|WORDPRESS_ENABLED=.*|WORDPRESS_ENABLED=true|" .env

# Add WordPress credentials if not exists
if ! grep -q "WORDPRESS_USERNAME" .env; then
    echo "" >> .env
    echo "# WordPress Credentials" >> .env
    echo "WORDPRESS_USERNAME=$wp_username" >> .env
    echo "WORDPRESS_PASSWORD=$wp_password" >> .env
else
    sed -i.bak "s|WORDPRESS_USERNAME=.*|WORDPRESS_USERNAME=$wp_username|" .env
    sed -i.bak "s|WORDPRESS_PASSWORD=.*|WORDPRESS_PASSWORD=$wp_password|" .env
fi

rm -f .env.bak

echo -e "${GREEN}✅ Configuration saved to .env${NC}"

# Update wordpress_config.yaml
echo ""
echo -e "${BLUE}📝 Updating wordpress_config.yaml...${NC}"

if [ -f config/wordpress_config.yaml ]; then
    # Using sed to update YAML (basic approach)
    sed -i.bak "s|site_url: \".*\"|site_url: \"$wp_url\"|" config/wordpress_config.yaml
    sed -i.bak "s|username: \".*\"|username: \"$wp_username\"|" config/wordpress_config.yaml
    rm -f config/wordpress_config.yaml.bak
    echo -e "${GREEN}✅ wordpress_config.yaml updated${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}✅ WordPress Setup Complete!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "📊 Configuration Summary:"
echo -e "   WordPress URL: $wp_url"
echo -e "   Username: $wp_username"
echo -e "   Status: ${GREEN}Connected ✓${NC}"
echo ""
echo -e "🚀 Next Steps:"
echo "   1. Run the server: ./scripts/run_agent.sh"
echo "   2. Try WordPress examples: python examples/wordpress_blog_agent.py"
echo "   3. Access WordPress dashboard: http://localhost:8000/wordpress"
echo ""
echo -e "${YELLOW}💡 Tip: You can modify settings in config/wordpress_config.yaml${NC}"
echo ""
