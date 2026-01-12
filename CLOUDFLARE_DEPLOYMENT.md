# Cloudflare Deployment Guide

This guide provides comprehensive instructions for deploying the UNLIMITED IRON CREATOR Streamlit application to Cloudflare infrastructure.

## Table of Contents
- [Deployment Options](#deployment-options)
- [Option 1: Cloudflare Pages (Recommended for Static Builds)](#option-1-cloudflare-pages)
- [Option 2: Cloudflare Workers (Advanced)](#option-2-cloudflare-workers)
- [Option 3: Cloudflare Tunnel + Docker (Full-Featured)](#option-3-cloudflare-tunnel--docker)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [Custom Domain Setup](#custom-domain-setup)
- [Troubleshooting](#troubleshooting)

## Deployment Options

Since UNLIMITED IRON CREATOR is a Streamlit application (Python-based web framework), there are several ways to deploy it on Cloudflare infrastructure:

### Quick Comparison

| Method | Best For | Complexity | Cost | Full Features |
|--------|----------|------------|------|---------------|
| **Cloudflare Tunnel + Docker** | Production, full features | Medium | Free tier available | ✅ Yes |
| **Cloudflare Pages** | Static previews, demos | Low | Free | ⚠️ Limited |
| **Cloudflare Workers** | Serverless, custom setup | High | Pay-as-you-go | ⚠️ Requires rewrite |

**Recommended**: Use **Cloudflare Tunnel + Docker** for the full Streamlit experience with all features.

---

## Option 1: Cloudflare Pages

Cloudflare Pages is designed for static sites. While Streamlit requires a server, you can use Cloudflare Pages to:
- Host documentation
- Deploy a static version if converted
- Use as a landing page that links to your app

### Prerequisites

1. **Cloudflare Account**
   - Sign up at [cloudflare.com](https://www.cloudflare.com)
   - Free tier available

2. **GitHub Repository**
   - Your code must be in a GitHub repository
   - Cloudflare Pages connects directly to GitHub

### Deployment Steps

#### Method A: Via Cloudflare Dashboard (Easiest)

1. **Log in to Cloudflare Dashboard**
   - Go to [dash.cloudflare.com](https://dash.cloudflare.com)
   - Navigate to "Workers & Pages" → "Pages"

2. **Create a New Project**
   - Click "Create a project"
   - Click "Connect to Git"
   - Authorize Cloudflare to access your GitHub account
   - Select the `UNLIMITED-IRON-CREATOR` repository

3. **Configure Build Settings**
   ```
   Production branch: main
   Build command: echo "Static deployment"
   Build output directory: /
   ```

4. **Environment Variables** (Optional)
   - Add any API keys or configuration:
   ```
   STREAMLIT_SERVER_PORT=8080
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   ```

5. **Deploy**
   - Click "Save and Deploy"
   - Your app will be available at: `https://unlimited-iron-creator.pages.dev`

#### Method B: Via Wrangler CLI

1. **Install Wrangler**
   ```bash
   npm install -g wrangler
   ```

2. **Login to Cloudflare**
   ```bash
   wrangler login
   ```

3. **Initialize Pages Project**
   ```bash
   cd /path/to/UNLIMITED-IRON-CREATOR
   wrangler pages project create unlimited-iron-creator
   ```

4. **Deploy**
   ```bash
   wrangler pages deploy . --project-name=unlimited-iron-creator
   ```

### Limitations with Pages

⚠️ **Important**: Cloudflare Pages is designed for static sites. Streamlit requires a Python server, so:
- Dynamic features won't work without additional setup
- Consider using this for documentation or as a landing page
- For full Streamlit functionality, use Cloudflare Tunnel (Option 3)

---

## Option 2: Cloudflare Workers

Cloudflare Workers is a serverless platform that can run JavaScript/TypeScript code at the edge. To use it with a Streamlit app, you would need to:

### Considerations

⚠️ **Complex Setup**: This requires significant application rewriting:
- Streamlit is Python-based; Workers primarily support JavaScript/WebAssembly
- You'd need to use Python Workers (experimental) or rewrite in JS
- Not recommended unless you have specific edge computing requirements

### If You Choose This Path

1. **Install Wrangler**
   ```bash
   npm install -g wrangler
   ```

2. **Create a New Worker**
   ```bash
   wrangler init unlimited-iron-creator
   ```

3. **Develop Your Worker**
   - You would need to rewrite the Streamlit app as a Worker
   - Consider using Python Workers (in beta): https://developers.cloudflare.com/workers/languages/python/

**Recommendation**: This approach is not recommended for this Streamlit application. Use Option 3 instead.

---

## Option 3: Cloudflare Tunnel + Docker (Recommended)

**This is the best option for running the full Streamlit application on Cloudflare infrastructure.**

Cloudflare Tunnel creates a secure connection from your server/container to Cloudflare's network, making your app accessible via Cloudflare's CDN and security features.

### Prerequisites

1. **Cloudflare Account** (Free tier works)
2. **Docker** installed on your server
3. **A server to run the container** (VPS, home server, etc.)

### Step-by-Step Guide

#### Step 1: Install Cloudflare Tunnel (cloudflared)

**On Linux/macOS:**
```bash
# Download and install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

# Verify installation
cloudflared --version
```

**On Windows:**
```powershell
# Download from: https://github.com/cloudflare/cloudflared/releases
# Or use chocolatey:
choco install cloudflared
```

**Via Docker:**
```bash
docker pull cloudflare/cloudflared:latest
```

#### Step 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This will:
- Open a browser window
- Ask you to select a domain/zone
- Download a certificate to `~/.cloudflared/cert.pem`

#### Step 3: Create a Tunnel

```bash
# Create a new tunnel
cloudflared tunnel create unlimited-iron-creator

# This creates a tunnel credentials file at:
# ~/.cloudflared/<TUNNEL-ID>.json
# Note the Tunnel ID for next steps
```

#### Step 4: Build and Run the Docker Container

```bash
# Navigate to the repository
cd /path/to/UNLIMITED-IRON-CREATOR

# Build the Docker image
docker build -t unlimited-iron-creator .

# Run the container
docker run -d \
  --name unlimited-iron-creator \
  -p 8080:8080 \
  --restart unless-stopped \
  unlimited-iron-creator

# Verify it's running
curl http://localhost:8080
```

#### Step 5: Configure the Tunnel

Create a configuration file at `~/.cloudflared/config.yml`:

```yaml
tunnel: unlimited-iron-creator
credentials-file: /home/YOUR_USER/.cloudflared/TUNNEL-ID.json

ingress:
  # Route all traffic to the Streamlit app
  - hostname: unlimited-iron-creator.yourdomain.com
    service: http://localhost:8080
  
  # Catch-all rule (required)
  - service: http_status:404
```

**Replace:**
- `YOUR_USER` with your username
- `TUNNEL-ID` with your actual tunnel ID
- `yourdomain.com` with your domain

#### Step 6: Create DNS Record

```bash
# Route your domain to the tunnel
cloudflared tunnel route dns unlimited-iron-creator unlimited-iron-creator.yourdomain.com
```

This automatically creates a CNAME record in Cloudflare DNS.

#### Step 7: Run the Tunnel

```bash
# Run the tunnel (foreground for testing)
cloudflared tunnel run unlimited-iron-creator

# Or run as a service (background)
cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

#### Step 8: Access Your App

Your Streamlit app is now accessible at:
```
https://unlimited-iron-creator.yourdomain.com
```

✅ **Benefits:**
- Full Streamlit functionality
- Cloudflare CDN and DDoS protection
- Free SSL/TLS certificates
- No need to expose ports directly to the internet
- Works behind NAT/firewall

### Using Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: unlimited-iron-creator
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    volumes:
      - ./generated_media:/app/generated_media

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    restart: unless-stopped
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${TUNNEL_TOKEN}
    depends_on:
      - app
```

Then run:
```bash
docker-compose up -d
```

---

## Configuration

### Environment Variables

Set these environment variables for your deployment:

```bash
# Application settings
export PORT=8080
export STREAMLIT_SERVER_PORT=8080
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false

# Optional: API keys for AI services
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

### Cloudflare Tunnel Configuration

Example `~/.cloudflared/config.yml`:

```yaml
tunnel: unlimited-iron-creator
credentials-file: /home/user/.cloudflared/abc123.json

ingress:
  # Main app
  - hostname: app.yourdomain.com
    service: http://localhost:8080
    originRequest:
      noTLSVerify: true
      connectTimeout: 30s
      
  # Health check endpoint
  - hostname: app.yourdomain.com
    path: /_stcore/health
    service: http://localhost:8080
  
  # Catch-all
  - service: http_status:404
```

---

## Custom Domain Setup

### If You Own a Domain

1. **Add Domain to Cloudflare**
   - Go to Cloudflare Dashboard
   - Click "Add a Site"
   - Follow the instructions to change your nameservers

2. **Create DNS Record** (via tunnel route command)
   ```bash
   cloudflared tunnel route dns unlimited-iron-creator app.yourdomain.com
   ```

3. **Access Your App**
   ```
   https://app.yourdomain.com
   ```

### If You Don't Own a Domain

You can use:
- Cloudflare's provided subdomain: `unlimited-iron-creator.pages.dev`
- Or register a free domain with providers like Freenom, and add it to Cloudflare

---

## Monitoring and Management

### View Tunnel Logs

```bash
# If running as service
sudo journalctl -u cloudflared -f

# If running in Docker
docker logs -f cloudflared-tunnel
```

### View Application Logs

```bash
docker logs -f unlimited-iron-creator
```

### Stop/Start Services

```bash
# Stop tunnel
sudo systemctl stop cloudflared

# Stop app
docker stop unlimited-iron-creator

# Start everything
sudo systemctl start cloudflared
docker start unlimited-iron-creator
```

### Update the Application

```bash
# Pull latest code
cd /path/to/UNLIMITED-IRON-CREATOR
git pull

# Rebuild and restart
docker build -t unlimited-iron-creator .
docker stop unlimited-iron-creator
docker rm unlimited-iron-creator
docker run -d \
  --name unlimited-iron-creator \
  -p 8080:8080 \
  --restart unless-stopped \
  unlimited-iron-creator
```

---

## Troubleshooting

### Issue: Tunnel won't connect

**Solutions:**
1. Check tunnel status:
   ```bash
   cloudflared tunnel info unlimited-iron-creator
   ```

2. Verify credentials file exists:
   ```bash
   ls ~/.cloudflared/
   ```

3. Check configuration:
   ```bash
   cloudflared tunnel validate ~/.cloudflared/config.yml
   ```

### Issue: App not accessible

**Solutions:**
1. Verify Docker container is running:
   ```bash
   docker ps | grep unlimited-iron-creator
   ```

2. Test local access:
   ```bash
   curl http://localhost:8080
   ```

3. Check tunnel logs:
   ```bash
   sudo journalctl -u cloudflared -f
   ```

### Issue: 502 Bad Gateway

**Solutions:**
1. Ensure the app is running on the correct port (8080)
2. Verify Streamlit is configured for headless mode
3. Check if the Docker container has enough resources

### Issue: DNS not resolving

**Solutions:**
1. Verify DNS record was created:
   ```bash
   cloudflared tunnel route dns list
   ```

2. Check Cloudflare DNS settings in the dashboard
3. Wait a few minutes for DNS propagation

### Issue: Performance issues

**Solutions:**
1. Increase Docker container resources:
   ```bash
   docker run -d \
     --name unlimited-iron-creator \
     -p 8080:8080 \
     --memory="2g" \
     --cpus="2" \
     unlimited-iron-creator
   ```

2. Enable Cloudflare caching for static assets
3. Use Cloudflare's Argo Smart Routing (paid feature)

---

## Security Best Practices

1. **Use Environment Variables for Secrets**
   - Never commit API keys to the repository
   - Use Docker secrets or environment files

2. **Enable Cloudflare Security Features**
   - Enable WAF (Web Application Firewall)
   - Set up rate limiting
   - Enable DDoS protection

3. **Keep Software Updated**
   ```bash
   # Update cloudflared
   cloudflared update
   
   # Update Docker image
   docker pull python:3.10-slim
   docker build -t unlimited-iron-creator .
   ```

4. **Use Access Control**
   - Set up Cloudflare Access for authentication
   - Restrict access by IP if needed

---

## Cost Estimation

### Cloudflare Free Tier Includes:
- Unlimited bandwidth
- DDoS protection
- Free SSL certificates
- Cloudflare Tunnel (free)
- Cloudflare Pages (500 builds/month)

### Additional Costs (Optional):
- **Cloudflare Pro**: $20/month (advanced features)
- **Cloudflare Workers**: $5/month + usage (if using Workers)
- **Server/VPS**: $5-50/month (for running Docker container)
  - DigitalOcean Droplet: $6/month (1GB RAM)
  - AWS EC2 t3.micro: ~$10/month
  - Hetzner Cloud: €3.79/month (2GB RAM)

**Total Estimated Cost**: Free - $30/month depending on hosting choice

---

## Next Steps

After successful deployment:

1. **Set up monitoring**: Use Cloudflare Analytics
2. **Configure caching**: Set up cache rules for better performance
3. **Enable security features**: WAF, rate limiting, bot protection
4. **Set up CI/CD**: Automate deployments with GitHub Actions
5. **Add custom domain**: Use your own domain name
6. **Configure backups**: Regularly backup your generated media
7. **Optimize performance**: Enable Argo, use Workers for edge logic

---

## Additional Resources

- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Docker Documentation](https://docs.docker.com/)

---

## Support

For issues specific to:
- **Cloudflare services**: [Cloudflare Community](https://community.cloudflare.com/)
- **This application**: [GitHub Issues](https://github.com/americaniron/UNLIMITED-IRON-CREATOR/issues)
- **Streamlit**: [Streamlit Community](https://discuss.streamlit.io/)

---

**Congratulations! Your UNLIMITED IRON CREATOR app is now running on Cloudflare infrastructure!** 🚀☁️
