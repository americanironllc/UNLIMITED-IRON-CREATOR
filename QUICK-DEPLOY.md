# Quick Deployment Reference

## 🚀 Deploy Now

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/americanironllc/UNLIMITED-IRON-CREATOR.git)

---

## ⚡ Quick Facts

| Aspect | Detail |
|--------|--------|
| **Deployment Time** | 3-5 minutes |
| **Manual Steps Required** | 0 |
| **Prerequisites** | Google Cloud account with billing |
| **Cost (Light Usage)** | $0-5/month (often FREE) |
| **Configuration Needed** | None (fully functional immediately) |
| **API Keys Required** | No (optional for real AI features) |

---

## 📋 What You Get

✅ **Instant Access**
- Live HTTPS URL
- Secure Google Cloud infrastructure
- Auto-scaling from 0 to 10 instances

✅ **Full Features**
- Streamlit web interface
- Text generation (sample/demo mode)
- Image generation (placeholder mode)
- Audio generation (placeholder mode)
- Video generation (placeholder mode)
- Project mode (all media types)
- History tracking
- Download functionality

✅ **Production Ready**
- 2GB RAM, 2 vCPUs
- Health checks configured
- Auto-scaling enabled
- 300-second timeout
- HTTPS with Google SSL

---

## 🔑 Optional: Add Real AI

After deployment, connect real AI services:

### Method 1: Google Secret Manager (Recommended)
```bash
# Create secrets
gcloud secrets create openai-api-key --data-file=-
gcloud secrets create elevenlabs-api-key --data-file=-

# Update service
gcloud run services update unlimited-iron-creator \
  --region us-central1 \
  --set-secrets="OPENAI_API_KEY=openai-api-key:latest"
```

### Method 2: Environment Variables
1. Go to Cloud Run Console
2. Select service → Edit & Deploy New Revision
3. Add environment variables:
   - `OPENAI_API_KEY`
   - `ELEVENLABS_API_KEY`
   - `STABILITY_API_KEY`

---

## 📊 Cost Breakdown

### Free Tier (Monthly)
- 2 million requests
- 360,000 GiB-seconds memory
- 180,000 vCPU-seconds

### Typical Costs
- **Personal Use** (<1k req/day): FREE
- **Small Team** (~5k req/day): $5-15
- **Medium** (~20k req/day): $20-50

### Cost Optimization
- Auto-scales to 0 when idle ✅
- Optimized container size ✅
- Efficient resource allocation ✅

---

## 🛠️ Management Commands

### View Service Info
```bash
gcloud run services describe unlimited-iron-creator --region us-central1
```

### View Logs
```bash
gcloud run services logs tail unlimited-iron-creator --region us-central1
```

### Update Service
```bash
gcloud run deploy unlimited-iron-creator --source . --region us-central1
```

### Delete Service
```bash
gcloud run services delete unlimited-iron-creator --region us-central1
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Button doesn't work** | Ensure billing is enabled on your Google Cloud account |
| **502 Bad Gateway** | Wait 30 seconds for cold start, then refresh |
| **504 Timeout** | App is starting, wait 1 minute and try again |
| **403 Forbidden** | Run: `gcloud run services add-iam-policy-binding unlimited-iron-creator --region=us-central1 --member="allUsers" --role="roles/run.invoker"` |
| **Build fails** | Check Cloud Build logs in console, usually permission issue |

---

## 📚 Documentation

- **[ONE-CLICK-DEPLOY.md](./ONE-CLICK-DEPLOY.md)** - Complete guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Advanced configuration
- **[README.md](./README.md)** - Main documentation
- **[DEPLOYMENT-CHECKLIST.md](./DEPLOYMENT-CHECKLIST.md)** - Technical verification

---

## ✅ Success Checklist

After clicking the button:

- [ ] Google Cloud Shell opened
- [ ] Repository cloned
- [ ] Docker build started
- [ ] Build completed (2-3 minutes)
- [ ] Service deployed
- [ ] Received URL: `https://unlimited-iron-creator-*.run.app`
- [ ] URL loads Streamlit interface
- [ ] Features work without errors

**Total Time: 3-5 minutes** ⏱️

---

## 🎯 Ready to Deploy?

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/americanironllc/UNLIMITED-IRON-CREATOR.git)

**One click. Zero configuration. Fully functional.** 🚀
