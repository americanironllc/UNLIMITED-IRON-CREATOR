# One-Click Deployment Guide

## 🚀 Deploy to Google Cloud Run in Minutes

This guide explains the one-click deployment process for UNLIMITED IRON CREATOR on Google Cloud Run.

---

## The One-Click Button

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/americanironllc/UNLIMITED-IRON-CREATOR.git)

Click this button to automatically deploy the application to Google Cloud Run with **zero manual configuration required**.

---

## What Happens When You Click?

### Step 1: Authentication
- You'll be redirected to Google Cloud Console
- Sign in with your Google account (or create one - it's free!)
- If you're new, you'll get **$300 in free credits** for 90 days

### Step 2: Project Setup
- Google Cloud will either use your existing project or help you create a new one
- Required APIs are automatically enabled:
  - Cloud Run API
  - Cloud Build API
  - Artifact Registry API

### Step 3: Automated Build
- The Dockerfile is automatically built by Cloud Build
- All dependencies from `requirements.txt` are installed
- The container image is stored in Google Artifact Registry
- **Takes ~2-3 minutes**

### Step 4: Deployment
- Cloud Run automatically deploys your container with optimized settings:
  - **Memory:** 2GB RAM
  - **CPU:** 2 vCPUs
  - **Scaling:** 0 to 10 instances (auto-scales based on traffic)
  - **Timeout:** 300 seconds
  - **Port:** 8080
  - **Authentication:** Public access (no login required)
- **Takes ~1-2 minutes**

### Step 5: Live URL
- You receive a secure HTTPS URL: `https://unlimited-iron-creator-[unique-id]-uc.a.run.app`
- The app is immediately accessible and fully functional
- **Total time: 3-5 minutes**

---

## Post-Deployment: The App is Ready!

### ✅ What Works Immediately

The application is **100% functional** right after deployment:

1. **Web Interface:** Beautiful Streamlit UI with all features
2. **Text Generation:** Creates sample text with metadata
3. **Image Generation:** Generates placeholders with detailed metadata
4. **Audio Generation:** Creates audio file placeholders with specs
5. **Video Generation:** Generates video file placeholders with params
6. **Project Mode:** Combines all media types
7. **History Tracking:** Tracks all your generations
8. **Download Functionality:** Export generated content

**The app works as a demonstration framework** without any API keys. It shows you exactly what would be generated when connected to real AI services.

### 🔑 Optional: Add Real AI Capabilities

To connect real AI services (OpenAI, ElevenLabs, Stable Diffusion, etc.), add your API keys:

#### Method 1: Using Google Secret Manager (Recommended)

1. **Create Secrets:**
   ```bash
   # Open Google Cloud Shell and replace the placeholder with your actual API key
   # echo -n prevents adding a newline character to the secret
   echo -n "sk-proj-..." | gcloud secrets create openai-api-key --data-file=-
   echo -n "abc123..." | gcloud secrets create elevenlabs-api-key --data-file=-
   echo -n "sk-..." | gcloud secrets create stability-api-key --data-file=-
   
   # Alternative: Interactive method (Cloud Shell will prompt for the secret)
   # gcloud secrets create openai-api-key
   ```

2. **Grant Access:**
   ```bash
   PROJECT_ID=$(gcloud config get-value project)
   SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"
   
   gcloud secrets add-iam-policy-binding openai-api-key \
     --member="serviceAccount:${SERVICE_ACCOUNT}" \
     --role="roles/secretmanager.secretAccessor"
   ```

3. **Update Cloud Run Service:**
   ```bash
   gcloud run services update unlimited-iron-creator \
     --region us-central1 \
     --set-secrets="OPENAI_API_KEY=openai-api-key:latest,ELEVENLABS_API_KEY=elevenlabs-api-key:latest,STABILITY_API_KEY=stability-api-key:latest"
   ```

#### Method 2: Using Environment Variables

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on your service: `unlimited-iron-creator`
3. Click **"EDIT & DEPLOY NEW REVISION"**
4. Scroll to **"Container, Variables & Secrets"** → **"Variables"**
5. Click **"ADD VARIABLE"** and add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ELEVENLABS_API_KEY`: Your ElevenLabs API key
   - `STABILITY_API_KEY`: Your Stability AI API key
6. Click **"DEPLOY"**

**Note:** Environment variables are visible in the console. Use Secret Manager for production deployments.

---

## Zero Manual Configuration Features

### Automatic Setup Includes:

✅ **Container Configuration**
- Dockerfile optimized for Cloud Run
- Multi-stage builds for smaller image size
- Python 3.10 with all dependencies

✅ **Service Configuration**
- Auto-scaling from 0 to 10 instances
- Health checks configured (`/_stcore/health`)
- Request timeout: 300 seconds
- Startup CPU boost enabled

✅ **Network Configuration**
- HTTPS endpoint with Google SSL certificate
- Public access enabled
- CORS configured for Streamlit

✅ **Resource Allocation**
- 2GB memory (optimal for Streamlit)
- 2 vCPUs (smooth performance)
- Gen2 execution environment (faster, more efficient)

✅ **Monitoring & Logging**
- Automatic request logging
- Performance metrics dashboard
- Error tracking and alerts

✅ **Security**
- Google Cloud's security infrastructure
- Automatic container scanning
- DDoS protection
- Rate limiting

---

## Access Your Deployed App

After deployment completes:

1. **Copy the URL** from the success message
2. **Open in browser:** `https://unlimited-iron-creator-[unique-id]-uc.a.run.app`
3. **Start creating:** The web interface is ready to use!

### Bookmarking Your App

- The URL is permanent and won't change
- Save it as a bookmark
- Share it with your team

---

## Managing Your Deployment

### View Service Details

```bash
gcloud run services describe unlimited-iron-creator --region us-central1
```

### View Logs

```bash
# Stream live logs
gcloud run services logs tail unlimited-iron-creator --region us-central1

# View recent logs
gcloud run services logs read unlimited-iron-creator --region us-central1
```

### Update the App

When there are updates to the repository:

```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1
```

Or simply click the deploy button again!

### Scale Configuration

Adjust scaling limits:

```bash
gcloud run services update unlimited-iron-creator \
  --region us-central1 \
  --min-instances 1 \
  --max-instances 20
```

### Delete the Service

If you want to remove the deployment:

```bash
gcloud run services delete unlimited-iron-creator --region us-central1
```

---

## Cost Information

### Free Tier (Per Month)
Google Cloud Run offers generous free tier:
- 2 million requests
- 360,000 GiB-seconds of memory
- 180,000 vCPU-seconds
- 1 GB network egress

### Typical Costs

**Personal Use (< 1000 requests/day):**
- Usually **FREE** within free tier limits
- Estimated: $0-2/month

**Small Team (~ 5000 requests/day):**
- Estimated: $5-15/month

**Medium Traffic (~ 20,000 requests/day):**
- Estimated: $20-50/month

### Cost Optimization

The deployment is pre-configured for cost efficiency:
- **Scale to zero:** No charges when app is idle
- **Auto-scaling:** Only pay for what you use
- **Optimized resources:** Right-sized for Streamlit

---

## Troubleshooting

### Deployment Fails

**Issue:** Build timeout
**Solution:** This is rare, but if it happens, click the button again. Cloud Build will use cached layers and complete faster.

**Issue:** Insufficient permissions
**Solution:** Ensure billing is enabled on your Google Cloud project.

### App Not Loading

**Issue:** 502 Bad Gateway
**Solution:** Wait 30 seconds for cold start. First request may take longer.

**Issue:** 504 Gateway Timeout
**Solution:** The app is still starting. Refresh after 1 minute.

### Can't Access URL

**Issue:** 403 Forbidden
**Solution:** The service deployed without public access. Run:
```bash
gcloud run services add-iam-policy-binding unlimited-iron-creator \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

---

## Advanced Options

### Custom Domain

Map your own domain:

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Select your service
3. Click **"MANAGE CUSTOM DOMAINS"**
4. Follow the verification steps
5. Update your DNS records

### CI/CD Integration

Automate deployments with GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: google-github-actions/deploy-cloudrun@main
        with:
          service: unlimited-iron-creator
          region: us-central1
          source: .
```

### Multiple Environments

Deploy separate instances for dev/staging/prod:

```bash
# Development
gcloud run deploy unlimited-iron-creator-dev \
  --source . \
  --region us-central1

# Production
gcloud run deploy unlimited-iron-creator-prod \
  --source . \
  --region us-central1 \
  --min-instances 1
```

---

## Support

### Getting Help

- **Cloud Run Documentation:** https://cloud.google.com/run/docs
- **Application Issues:** Open an issue on [GitHub](https://github.com/americanironllc/UNLIMITED-IRON-CREATOR/issues)
- **Deployment Issues:** Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting

### Quick Support Checklist

Before asking for help:
1. Check the Cloud Run service logs
2. Verify billing is enabled
3. Ensure required APIs are enabled
4. Try redeploying with the button

---

## Summary

The one-click deployment provides:

✅ **Zero Configuration:** No manual setup required  
✅ **Fully Functional:** App works immediately  
✅ **Production Ready:** Optimized settings included  
✅ **Secure by Default:** HTTPS, DDoS protection, security scanning  
✅ **Cost Effective:** Likely free with included credits  
✅ **Scalable:** Auto-scales from 0 to 10 instances  
✅ **Easy Updates:** Just click the button again  

**Click the button, wait 5 minutes, and you're live!** 🚀

---

**Ready to deploy?**

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/americanironllc/UNLIMITED-IRON-CREATOR.git)
