#!/bin/bash

# Cloudflare Deployment Helper Script
# This script helps you set up and deploy UNLIMITED IRON CREATOR to Cloudflare

set -e

echo "=============================================="
echo "UNLIMITED IRON CREATOR - Cloudflare Deployment"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if cloudflared is installed
check_cloudflared() {
    if ! command -v cloudflared &> /dev/null; then
        echo -e "${RED}❌ cloudflared is not installed${NC}"
        echo ""
        echo "Please install cloudflared first:"
        echo "  Linux/macOS: wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        echo "  Or visit: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
        exit 1
    fi
    echo -e "${GREEN}✓ cloudflared is installed${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        echo ""
        echo "Please install Docker first:"
        echo "  Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker is installed${NC}"
}

# Display menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo "1) First-time setup (authenticate and create tunnel)"
    echo "2) Build and run Docker container"
    echo "3) Deploy with Docker Compose"
    echo "4) Start Cloudflare tunnel"
    echo "5) View logs"
    echo "6) Stop services"
    echo "7) Complete deployment (all steps)"
    echo "8) Show deployment status"
    echo "9) Exit"
    echo ""
    read -p "Enter your choice [1-9]: " choice
}

# First-time setup
first_time_setup() {
    echo ""
    echo -e "${YELLOW}Starting first-time setup...${NC}"
    echo ""
    
    # Login to Cloudflare
    echo "Step 1: Authenticate with Cloudflare"
    cloudflared tunnel login
    echo -e "${GREEN}✓ Authenticated${NC}"
    echo ""
    
    # Create tunnel
    echo "Step 2: Create a new tunnel"
    read -p "Enter a name for your tunnel (default: unlimited-iron-creator): " tunnel_name
    tunnel_name=${tunnel_name:-unlimited-iron-creator}
    
    cloudflared tunnel create "$tunnel_name"
    echo -e "${GREEN}✓ Tunnel created: $tunnel_name${NC}"
    echo ""
    
    # Get tunnel info
    tunnel_id=$(cloudflared tunnel list | grep "$tunnel_name" | awk '{print $1}')
    echo "Tunnel ID: $tunnel_id"
    echo ""
    
    # Configure DNS
    echo "Step 3: Configure DNS"
    read -p "Enter your domain (e.g., app.yourdomain.com): " domain
    
    cloudflared tunnel route dns "$tunnel_name" "$domain"
    echo -e "${GREEN}✓ DNS configured for $domain${NC}"
    echo ""
    
    # Create config file
    echo "Step 4: Creating configuration file"
    config_file="$HOME/.cloudflared/config.yml"
    
    cat > "$config_file" << EOF
tunnel: $tunnel_id
credentials-file: $HOME/.cloudflared/$tunnel_id.json

ingress:
  - hostname: $domain
    service: http://localhost:8080
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s
  - service: http_status:404
EOF
    
    echo -e "${GREEN}✓ Config file created at $config_file${NC}"
    echo ""
    
    echo -e "${GREEN}First-time setup complete!${NC}"
    echo "Next steps:"
    echo "  1. Run option 2 to build and start the Docker container"
    echo "  2. Run option 4 to start the Cloudflare tunnel"
    echo "  3. Visit https://$domain"
}

# Build and run Docker container
build_and_run() {
    echo ""
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t unlimited-iron-creator .
    echo -e "${GREEN}✓ Image built${NC}"
    echo ""
    
    echo -e "${YELLOW}Starting Docker container...${NC}"
    docker stop unlimited-iron-creator 2>/dev/null || true
    docker rm unlimited-iron-creator 2>/dev/null || true
    
    docker run -d \
        --name unlimited-iron-creator \
        -p 8080:8080 \
        --restart unless-stopped \
        -v "$(pwd)/generated_media:/app/generated_media" \
        unlimited-iron-creator
    
    echo -e "${GREEN}✓ Container started${NC}"
    echo ""
    
    echo "Waiting for app to be ready..."
    sleep 5
    
    if curl -f http://localhost:8080 &>/dev/null; then
        echo -e "${GREEN}✓ App is running on http://localhost:8080${NC}"
    else
        echo -e "${YELLOW}⚠ App might still be starting up...${NC}"
    fi
}

# Deploy with Docker Compose
deploy_compose() {
    echo ""
    echo -e "${YELLOW}Deploying with Docker Compose...${NC}"
    
    if [ ! -f "docker-compose.cloudflare.yml" ]; then
        echo -e "${RED}❌ docker-compose.cloudflare.yml not found${NC}"
        exit 1
    fi
    
    read -p "Enter your Cloudflare Tunnel Token (or press Enter to skip): " tunnel_token
    
    if [ -n "$tunnel_token" ]; then
        export TUNNEL_TOKEN="$tunnel_token"
        docker-compose -f docker-compose.cloudflare.yml up -d
    else
        docker-compose -f docker-compose.cloudflare.yml up -d app
        echo -e "${YELLOW}Note: Tunnel not started. Run option 4 to start manually.${NC}"
    fi
    
    echo -e "${GREEN}✓ Services started${NC}"
}

# Start tunnel
start_tunnel() {
    echo ""
    echo -e "${YELLOW}Starting Cloudflare tunnel...${NC}"
    
    read -p "Enter tunnel name (default: unlimited-iron-creator): " tunnel_name
    tunnel_name=${tunnel_name:-unlimited-iron-creator}
    
    echo "Starting tunnel in the background..."
    echo "Use 'cloudflared tunnel run $tunnel_name' to run in foreground"
    echo "Or check logs with option 5"
    
    cloudflared service install
    sudo systemctl start cloudflared
    echo -e "${GREEN}✓ Tunnel started${NC}"
}

# View logs
view_logs() {
    echo ""
    echo "Which logs would you like to view?"
    echo "1) Application logs (Docker)"
    echo "2) Cloudflare tunnel logs"
    echo "3) Both"
    read -p "Enter choice [1-3]: " log_choice
    
    case $log_choice in
        1)
            echo -e "${YELLOW}Application logs:${NC}"
            docker logs -f unlimited-iron-creator
            ;;
        2)
            echo -e "${YELLOW}Tunnel logs:${NC}"
            sudo journalctl -u cloudflared -f
            ;;
        3)
            echo -e "${YELLOW}Opening logs in split view...${NC}"
            echo "Press Ctrl+C to exit"
            docker logs -f unlimited-iron-creator &
            sudo journalctl -u cloudflared -f
            ;;
        *)
            echo "Invalid choice"
            ;;
    esac
}

# Stop services
stop_services() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    
    docker stop unlimited-iron-creator 2>/dev/null || true
    sudo systemctl stop cloudflared 2>/dev/null || true
    docker-compose -f docker-compose.cloudflare.yml down 2>/dev/null || true
    
    echo -e "${GREEN}✓ Services stopped${NC}"
}

# Complete deployment
complete_deployment() {
    echo ""
    echo -e "${YELLOW}Starting complete deployment...${NC}"
    echo ""
    
    first_time_setup
    echo ""
    build_and_run
    echo ""
    start_tunnel
    echo ""
    
    echo -e "${GREEN}=============================================="
    echo "✓ Deployment complete!"
    echo "==============================================${NC}"
    echo ""
    echo "Your application should now be accessible via your configured domain."
}

# Show status
show_status() {
    echo ""
    echo -e "${YELLOW}Deployment Status${NC}"
    echo "===================="
    echo ""
    
    # Docker container status
    if docker ps | grep -q unlimited-iron-creator; then
        echo -e "Docker Container: ${GREEN}Running ✓${NC}"
    else
        echo -e "Docker Container: ${RED}Stopped ✗${NC}"
    fi
    
    # Cloudflare tunnel status
    if systemctl is-active --quiet cloudflared 2>/dev/null; then
        echo -e "Cloudflare Tunnel: ${GREEN}Running ✓${NC}"
    else
        echo -e "Cloudflare Tunnel: ${RED}Stopped ✗${NC}"
    fi
    
    # List tunnels
    echo ""
    echo "Available tunnels:"
    cloudflared tunnel list 2>/dev/null || echo "No tunnels found or cloudflared not configured"
    
    # App accessibility
    echo ""
    if curl -f http://localhost:8080 &>/dev/null; then
        echo -e "Local Access: ${GREEN}http://localhost:8080 ✓${NC}"
    else
        echo -e "Local Access: ${RED}Not accessible ✗${NC}"
    fi
}

# Main script
main() {
    echo "Checking prerequisites..."
    check_cloudflared
    check_docker
    echo ""
    
    while true; do
        show_menu
        
        case $choice in
            1) first_time_setup ;;
            2) build_and_run ;;
            3) deploy_compose ;;
            4) start_tunnel ;;
            5) view_logs ;;
            6) stop_services ;;
            7) complete_deployment ;;
            8) show_status ;;
            9) 
                echo "Goodbye!"
                exit 0
                ;;
            *)
                echo "Invalid choice. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main
