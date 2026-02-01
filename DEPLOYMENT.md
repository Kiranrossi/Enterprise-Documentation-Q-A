# 🚀 Deploying to Streamlit Cloud

This guide will help you deploy the Enterprise RAG System to Streamlit Cloud.

## ⚠️ Important Note

**This application requires Endee Vector Database to function.** Since Streamlit Cloud doesn't support Docker, you have two options:

### Option 1: Use Cloud-Hosted Endee (Recommended for Production)

If you have access to a cloud-hosted Endee instance:

1. Deploy Endee on a cloud server (AWS, GCP, Azure, DigitalOcean, etc.)
2. Configure the Endee URL in Streamlit Cloud secrets

### Option 2: Demo Mode (For Testing Only)

For demonstration purposes, you can run this locally and share via `streamlit run app.py --server.enableCORS=false`

---

## 📋 Prerequisites

- GitHub account
- Streamlit Cloud account ([sign up free](https://streamlit.io/cloud))
- Groq API key ([get free](https://console.groq.com))
- Cloud-hosted Endee instance (optional, for full functionality)

---

## 🔧 Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Enterprise RAG System"

# Add remote
git remote add origin https://github.com/Kiranrossi/Enterprise-Documentation-Q-A.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Click "New app"**

3. **Configure deployment:**
   - **Repository**: `Kiranrossi/Enterprise-Documentation-Q-A`
   - **Branch**: `main`
   - **Main file path**: `app.py`

4. **Click "Deploy"**

### Step 3: Configure Secrets

1. **In Streamlit Cloud dashboard, go to your app settings**

2. **Click "Secrets"**

3. **Add the following secrets:**

```toml
# Groq API Key (Required)
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"

# LLM Configuration
LLM_PROVIDER = "groq"
LLM_MODEL = "llama-3.3-70b-versatile"

# Endee Configuration (if using cloud-hosted Endee)
ENDEE_BASE_URL = "https://your-endee-instance.com/api/v1"
ENDEE_AUTH_TOKEN = "your_endee_auth_token"

# Or for local testing (won't work on Streamlit Cloud)
# ENDEE_HOST = "localhost"
# ENDEE_PORT = "8080"
```

4. **Click "Save"**

### Step 4: Verify Deployment

1. Wait for the app to build (2-3 minutes)
2. Check for any errors in the logs
3. Test the application

---

## 🐳 Deploying Endee to Cloud

Since Streamlit Cloud doesn't support Docker, you need to host Endee separately.

### Option A: DigitalOcean Droplet

```bash
# 1. Create a droplet (Ubuntu 22.04, $6/month)

# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone your repo
git clone https://github.com/Kiranrossi/Enterprise-Documentation-Q-A.git
cd Enterprise-Documentation-Q-A

# 5. Start Endee
docker compose up -d

# 6. Configure firewall to allow port 8080
ufw allow 8080

# 7. Get your public IP
curl ifconfig.me

# 8. Update Streamlit secrets with:
# ENDEE_BASE_URL = "http://YOUR_DROPLET_IP:8080/api/v1"
```

### Option B: Railway.app (Easiest)

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Deploy the `docker-compose.yml`
4. Get the public URL
5. Update Streamlit secrets

### Option C: AWS EC2

```bash
# 1. Launch EC2 instance (t2.micro for testing)
# 2. Install Docker
# 3. Run Endee container
# 4. Configure security group to allow port 8080
# 5. Use public IP in Streamlit secrets
```

---

## 🔒 Security Best Practices

### 1. Secure Endee Access

If exposing Endee to the internet:

```bash
# Add authentication token
docker run -d \
  -p 8080:8080 \
  -e ENDEE_AUTH_TOKEN="your-secure-token" \
  endee/endee:latest
```

Then in Streamlit secrets:
```toml
ENDEE_AUTH_TOKEN = "your-secure-token"
```

### 2. Use HTTPS

Set up a reverse proxy with SSL:

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name endee.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
    }
}
```

### 3. Environment Variables

Never commit `.env` or `secrets.toml` to GitHub!

---

## 🧪 Testing Deployment

### Local Testing Before Deploy

```bash
# Test with production-like settings
streamlit run app.py --server.port 8501 --server.enableCORS false
```

### After Deployment

1. **Upload a test document**
2. **Index it**
3. **Ask a question**
4. **Verify answer and sources**

---

## 📊 Monitoring

### Streamlit Cloud Logs

- View real-time logs in Streamlit Cloud dashboard
- Check for errors during indexing/querying

### Endee Monitoring

```bash
# Check Endee logs
docker logs endee

# Check Endee status
curl http://your-endee-url/api/v1/index/list
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused to Endee"

**Solution:**
- Verify Endee is running: `docker ps`
- Check firewall allows port 8080
- Verify `ENDEE_BASE_URL` in secrets is correct

### Issue: "Groq API Error"

**Solution:**
- Verify API key in secrets
- Check Groq quota at console.groq.com

### Issue: "Module not found"

**Solution:**
- Ensure all dependencies in `requirements.txt`
- Check Streamlit Cloud build logs

### Issue: "Out of memory"

**Solution:**
- Reduce `MAX_CHUNK_SIZE` in config
- Use smaller embedding model
- Upgrade Streamlit Cloud tier

---

## 💰 Cost Estimation

### Free Tier (Testing)

- **Streamlit Cloud**: Free (1 app)
- **Groq API**: Free tier (limited requests)
- **Endee**: Self-hosted on free tier cloud (DigitalOcean $0 credit)

**Total: $0/month** (with free credits)

### Production Tier

- **Streamlit Cloud**: $20/month (unlimited apps)
- **Groq API**: Pay-as-you-go (~$0.10/1K requests)
- **Endee Hosting**: $6-12/month (DigitalOcean droplet)

**Total: ~$30-35/month**

---

## 🔄 Continuous Deployment

Streamlit Cloud auto-deploys on every push to `main`:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Streamlit Cloud automatically rebuilds
```

---

## 📱 Sharing Your App

Once deployed, share your app:

```
https://your-app-name.streamlit.app
```

### Custom Domain (Optional)

1. Go to Streamlit Cloud settings
2. Add custom domain
3. Configure DNS records

---

## 🎯 Next Steps

After successful deployment:

1. ✅ Test all features
2. ✅ Monitor performance
3. ✅ Set up analytics
4. ✅ Add more documents
5. ✅ Share with users!

---

## 📞 Support

- **Streamlit Cloud**: [docs.streamlit.io](https://docs.streamlit.io)
- **Endee**: [endee.io/docs](https://endee.io/docs)
- **Groq**: [console.groq.com/docs](https://console.groq.com/docs)

---

**Happy Deploying! 🚀**
