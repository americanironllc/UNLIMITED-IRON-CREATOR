# Google Cloud Run Deployment Guide

This guide provides comprehensive instructions for deploying the UNLIMITED IRON CREATOR Streamlit application to Google Cloud Run.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Deploy](#quick-deploy)
- [Step-by-Step Deployment](#step-by-step-deployment)
- [Configuration Options](#configuration-options)
- [Environment Variables and Secrets](#environment-variables-and-secrets)
- [Post-Deployment](#post-deployment)
- [Cost Estimation](#cost-estimation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying to Google Cloud Run, ensure you have:

1. **Google Cloud Account**
   - Sign up at [cloud.google.com](https://cloud.google.com)
   - Enable billing for your account

2. **Google Cloud Project**
   - Create a new project in the [Google Cloud Console](https://console.cloud.google.com)
   - Note your Project ID (you'll need this for deployment)

3. **Google Cloud CLI (gcloud)**
   - Install: `curl https://sdk.cloud.google.com | bash`
   - Or download from: https://cloud.google.com/sdk/docs/install
   - Initialize: `gcloud init`
   - Authenticate: `gcloud auth login`

4. **Enable Required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   ```

5. **Set Your Project**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

## Quick Deploy

For the fastest deployment with recommended settings:

```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

This command will:
- Build the Docker image from the current directory
- Deploy to Cloud Run in the `us-central1` region
- Configure the service with 2GB RAM, 2 CPUs, and 5-minute timeout
- Make the app publicly accessible

**After deployment completes, you'll receive a URL where your app is running!**

## Step-by-Step Deployment

### Step 1: Prepare Your Code

Ensure you're in the project directory:
```bash
cd /path/to/UNLIMITED-IRON-CREATOR
```

### Step 2: Test Locally (Optional)

Test the Docker container locally before deploying:

```bash
# Build the Docker image
docker build -t unlimited-iron-creator .

# Run locally
docker run -p 8080:8080 unlimited-iron-creator

# Visit http://localhost:8080 in your browser
```

### Step 3: Configure Deployment Settings

Choose your region (closer to your users = better performance):
- `us-central1` (Iowa)
- `us-east1` (South Carolina)
- `us-west1` (Oregon)
- `europe-west1` (Belgium)
- `asia-east1` (Taiwan)
- See all regions: `gcloud run regions list`

### Step 4: Deploy to Cloud Run

**Basic deployment:**
```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

**Recommended deployment with optimized settings:**
```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0
```

### Step 5: Verify Deployment

After deployment, you'll see output like:
```
Service [unlimited-iron-creator] revision [unlimited-iron-creator-00001-xyz] has been deployed and is serving 100 percent of traffic.
Service URL: https://unlimited-iron-creator-xyz-uc.a.run.app
```

Visit the Service URL to access your app!

## Configuration Options

### Memory Settings

Streamlit apps can be memory-intensive. Recommended settings:

```bash
# Light usage (simple apps)
--memory 1Gi

# Medium usage (recommended for this app)
--memory 2Gi

# Heavy usage (complex visualizations)
--memory 4Gi
```

### CPU Settings

Configure CPU allocation:

```bash
# 1 CPU (default)
--cpu 1

# 2 CPUs (recommended for this app)
--cpu 2

# 4 CPUs (for compute-intensive operations)
--cpu 4
```

### Timeout Settings

Maximum request duration:

```bash
# Default (300 seconds / 5 minutes)
--timeout 300

# Extended for long-running operations
--timeout 600

# Maximum allowed
--timeout 3600
```

### Concurrency Settings

Requests per container instance:

```bash
# Default (80 concurrent requests)
--concurrency 80

# Conservative (better for resource-intensive apps)
--concurrency 10

# Maximum
--concurrency 1000
```

### Scaling Settings

Control auto-scaling behavior:

```bash
# Scale to zero when not in use (cost-effective)
--min-instances 0 --max-instances 10

# Always keep 1 instance warm (faster response)
--min-instances 1 --max-instances 10

# High traffic configuration
--min-instances 2 --max-instances 100
```

### Authentication

Control who can access your app:

```bash
# Public access (anyone can access)
--allow-unauthenticated

# Require authentication
--no-allow-unauthenticated
```

## Environment Variables and Secrets

### Setting Environment Variables

For non-sensitive configuration:

```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --set-env-vars "ENVIRONMENT=production,DEBUG=false"
```

### Using Secret Manager (Recommended for API Keys)

For sensitive data like API keys:

**Step 1: Create secrets in Secret Manager**

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create a secret for OpenAI API key
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Create other secrets as needed
echo -n "your-api-key" | gcloud secrets create other-api-key --data-file=-
```

**Step 2: Grant Cloud Run access to secrets**

```bash
# Get the Cloud Run service account
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"

# Grant access to the secret
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

**Step 3: Deploy with secrets**

```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --set-secrets="OPENAI_API_KEY=openai-api-key:latest"
```

### Complete Example with Environment Variables and Secrets

```bash
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars "ENVIRONMENT=production,APP_NAME=UNLIMITED-IRON-CREATOR" \
  --set-secrets="OPENAI_API_KEY=openai-api-key:latest,OTHER_API_KEY=other-api-key:latest"
```

## Post-Deployment

### Accessing Your App

Your app will be available at the URL provided after deployment:
```
https://unlimited-iron-creator-[hash]-[region].a.run.app
```

### Viewing Logs

Monitor your application logs:

```bash
# Stream logs in real-time
gcloud run services logs tail unlimited-iron-creator --region us-central1

# View recent logs
gcloud run services logs read unlimited-iron-creator --region us-central1 --limit 50
```

View logs in Cloud Console:
1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on your service
3. Click "LOGS" tab

### Updating the Deployment

To deploy updates:

```bash
# Make your code changes, then redeploy
gcloud run deploy unlimited-iron-creator \
  --source . \
  --region us-central1
```

Cloud Run will:
- Build a new container image
- Deploy with zero downtime
- Gradually shift traffic to the new revision

### Managing Revisions

```bash
# List all revisions
gcloud run revisions list --service unlimited-iron-creator --region us-central1

# Rollback to a previous revision
gcloud run services update-traffic unlimited-iron-creator \
  --to-revisions REVISION_NAME=100 \
  --region us-central1

# Delete old revisions
gcloud run revisions delete REVISION_NAME --region us-central1
```

### Setting Up Custom Domain (Optional)

**Step 1: Verify domain ownership**
1. Go to [Cloud Run Domain Mappings](https://console.cloud.google.com/run/domains)
2. Click "ADD MAPPING"
3. Follow verification steps

**Step 2: Map domain to service**
```bash
gcloud run domain-mappings create \
  --service unlimited-iron-creator \
  --domain yourdomain.com \
  --region us-central1
```

**Step 3: Update DNS**
Add the DNS records shown in the console to your domain provider.

### Monitoring and Metrics

View metrics in the Cloud Console:
1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on your service
3. View metrics for:
   - Request count
   - Request latency
   - Container instance count
   - CPU utilization
   - Memory utilization

## Cost Estimation

Cloud Run pricing is based on:
- CPU usage (per vCPU-second)
- Memory usage (per GiB-second)
- Requests (per million requests)
- Network egress

### Free Tier (per month)
- 2 million requests
- 360,000 GiB-seconds of memory
- 180,000 vCPU-seconds
- 1 GB network egress from North America

### Example Cost Estimates

**Light Usage** (1,000 requests/day, 2GB RAM, 2 CPUs, avg 2s request):
- ~$3-5 per month (likely within free tier)

**Medium Usage** (10,000 requests/day, 2GB RAM, 2 CPUs, avg 2s request):
- ~$15-25 per month

**Heavy Usage** (100,000 requests/day, 2GB RAM, 2 CPUs, avg 2s request):
- ~$100-150 per month

### Cost Optimization Tips

1. **Use `--min-instances 0`** to scale to zero when idle
2. **Set appropriate `--max-instances`** to control costs
3. **Optimize container startup time** to reduce cold start costs
4. **Use caching** to reduce CPU and memory usage
5. **Monitor and adjust** memory/CPU based on actual usage

### Monitoring Costs

```bash
# View cost breakdown
gcloud billing accounts list
gcloud billing projects link PROJECT_ID --billing-account BILLING_ACCOUNT_ID
```

View detailed billing in [Cloud Console Billing](https://console.cloud.google.com/billing)

## Troubleshooting

### Common Issues and Solutions

#### Issue: Deployment fails with "build error"

**Solution:**
```bash
# Check Dockerfile syntax
docker build -t test .

# Check build logs
gcloud builds list
gcloud builds log BUILD_ID
```

#### Issue: "Port configuration error"

**Solution:**
Ensure your Dockerfile correctly sets the PORT environment variable and Streamlit listens on it:
```dockerfile
ENV PORT=8080
CMD streamlit run streamlit_app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
```

#### Issue: App times out or returns 504

**Solutions:**
1. Increase timeout:
   ```bash
   --timeout 600
   ```

2. Increase resources:
   ```bash
   --memory 4Gi --cpu 4
   ```

3. Check application logs for errors:
   ```bash
   gcloud run services logs tail unlimited-iron-creator --region us-central1
   ```

#### Issue: Out of memory errors

**Solutions:**
1. Increase memory allocation:
   ```bash
   --memory 4Gi
   ```

2. Optimize your application to use less memory

3. Check memory usage in metrics

#### Issue: "Permission denied" errors

**Solution:**
Ensure proper IAM permissions:
```bash
# Grant yourself necessary roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/run.admin"
```

#### Issue: Slow cold starts

**Solutions:**
1. Use `--min-instances 1` to keep one instance warm
2. Optimize Docker image size
3. Use Cloud Build caching

#### Issue: Cannot access after deployment

**Solutions:**
1. Check if `--allow-unauthenticated` was set:
   ```bash
   gcloud run services add-iam-policy-binding unlimited-iron-creator \
     --region=us-central1 \
     --member="allUsers" \
     --role="roles/run.invoker"
   ```

2. Check service status:
   ```bash
   gcloud run services describe unlimited-iron-creator --region us-central1
   ```

#### Issue: Application crashes on startup

**Solution:**
1. Check logs:
   ```bash
   gcloud run services logs read unlimited-iron-creator --region us-central1 --limit 100
   ```

2. Test locally first:
   ```bash
   docker build -t test . && docker run -p 8080:8080 test
   ```

### Getting Help

- **Cloud Run Documentation**: https://cloud.google.com/run/docs
- **Stack Overflow**: Tag questions with `google-cloud-run` and `streamlit`
- **Google Cloud Support**: Available with paid support plans
- **Community Support**: https://cloud.google.com/support/community

### Useful Commands

```bash
# Get service details
gcloud run services describe unlimited-iron-creator --region us-central1

# List all Cloud Run services
gcloud run services list

# Delete service
gcloud run services delete unlimited-iron-creator --region us-central1

# Set default region
gcloud config set run/region us-central1

# View quotas
gcloud run services quotas list

# Test with curl
curl https://your-service-url.run.app

# Check service health
curl https://your-service-url.run.app/_stcore/health
```

## Best Practices

1. **Start Small**: Begin with minimal resources and scale up based on actual usage
2. **Use Secrets**: Never hardcode API keys or sensitive data
3. **Monitor Regularly**: Set up alerts for errors and unusual resource usage
4. **Test Locally**: Always test Docker builds locally before deploying
5. **Version Control**: Keep your deployment configurations in version control
6. **Set Budgets**: Configure billing alerts to avoid unexpected costs
7. **Use Tags**: Tag revisions for easier management
8. **Document Changes**: Keep track of configuration changes

## Next Steps

After successful deployment:

1. **Set up monitoring and alerting**
2. **Configure a custom domain** (optional)
3. **Implement CI/CD pipeline** for automated deployments
4. **Set up staging environment** for testing
5. **Review security settings** and access controls
6. **Optimize performance** based on metrics
7. **Set up backup and disaster recovery** procedures

---

**Congratulations! Your UNLIMITED IRON CREATOR app is now running on Google Cloud Run!** 🚀

For questions or issues specific to this application, please refer to the main README.md or open an issue on GitHub.
