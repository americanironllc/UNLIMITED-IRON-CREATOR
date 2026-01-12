# Cloudflare Quick Start Guide

This is a quick reference for deploying UNLIMITED IRON CREATOR to Cloudflare. For detailed instructions, see [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md).

## 🚀 Fast Track Deployment

### Prerequisites
- Cloudflare account (free tier works)
- Docker installed
- Domain name (optional but recommended)

### Method 1: Automated Script (Recommended)

```bash
# Make script executable
chmod +x deploy-cloudflare.sh

# Run the deployment script
./deploy-cloudflare.sh

# Follow the interactive prompts:
# 1. First-time setup
# 2. Build and run Docker
# 3. Start tunnel
```

### Method 2: Manual Steps

#### Step 1: Install Cloudflare Tunnel

```bash
# Linux/macOS
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

#### Step 2: Authenticate

```bash
cloudflared tunnel login
```

#### Step 3: Create Tunnel

```bash
cloudflared tunnel create unlimited-iron-creator
```

#### Step 4: Build and Run App

```bash
# Build Docker image
docker build -t unlimited-iron-creator .

# Run container
docker run -d \
  --name unlimited-iron-creator \
  -p 8080:8080 \
  --restart unless-stopped \
  unlimited-iron-creator
```

#### Step 5: Configure DNS

```bash
# Replace 'app.yourdomain.com' with your domain
cloudflared tunnel route dns unlimited-iron-creator app.yourdomain.com
```

#### Step 6: Create Config

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: ~/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: app.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

#### Step 7: Start Tunnel

```bash
cloudflared tunnel run unlimited-iron-creator
```

### Method 3: Docker Compose

```bash
# Get your tunnel token
cloudflared tunnel token unlimited-iron-creator

# Set environment variable
export TUNNEL_TOKEN="your_token_here"

# Deploy
docker-compose -f docker-compose.cloudflare.yml up -d
```

## 🔍 Verify Deployment

```bash
# Check container status
docker ps | grep unlimited-iron-creator

# Check tunnel status
cloudflared tunnel info unlimited-iron-creator

# Test local access
curl http://localhost:8080

# Access via domain
# Open: https://app.yourdomain.com
```

## 📊 Manage Services

```bash
# View logs
docker logs -f unlimited-iron-creator
journalctl -u cloudflared -f

# Restart services
docker restart unlimited-iron-creator
systemctl restart cloudflared

# Stop services
docker stop unlimited-iron-creator
systemctl stop cloudflared
```

## 🛠️ Troubleshooting

### App not accessible locally
```bash
# Check if container is running
docker ps

# View container logs
docker logs unlimited-iron-creator

# Restart container
docker restart unlimited-iron-creator
```

### Tunnel not connecting
```bash
# Check tunnel status
cloudflared tunnel info unlimited-iron-creator

# View tunnel logs
journalctl -u cloudflared -f

# Restart tunnel
systemctl restart cloudflared
```

### DNS not resolving
```bash
# Check DNS routes
cloudflared tunnel route dns list

# Wait a few minutes for propagation
# Check DNS: nslookup app.yourdomain.com
```

## 📚 Next Steps

- ✅ **Deployed?** Great! Visit your domain to access the app
- 📖 **Need more details?** Read [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md)
- 🔒 **Security:** Set up Cloudflare Access for authentication
- 📊 **Monitoring:** Enable Cloudflare Analytics
- 🚀 **Performance:** Configure caching rules

## 💡 Tips

1. **Free Tier**: Everything you need is available on Cloudflare's free tier
2. **No Port Forwarding**: Cloudflare Tunnel works behind NAT/firewall
3. **SSL Included**: Free SSL certificates for your domain
4. **DDoS Protection**: Automatic DDoS protection included
5. **Global CDN**: Your app is served from Cloudflare's global network

## 🆘 Need Help?

- 📖 Read the full guide: [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/americaniron/UNLIMITED-IRON-CREATOR/issues)
- 💬 Cloudflare Community: [community.cloudflare.com](https://community.cloudflare.com/)
- 📚 Cloudflare Docs: [developers.cloudflare.com](https://developers.cloudflare.com/)

---

**Ready to deploy? Run `./deploy-cloudflare.sh` to get started!** 🚀
