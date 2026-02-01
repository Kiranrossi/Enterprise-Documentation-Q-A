# ✅ Streamlit Cloud Deployment Checklist

## 📋 Pre-Deployment

- [x] Code pushed to GitHub
- [ ] Groq API key ready
- [ ] Endee instance accessible (optional for demo)

---

## 🚀 Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud

Visit: **[share.streamlit.io](https://share.streamlit.io)**

### Step 2: Create New App

Click **"New app"** button

### Step 3: Configure App

Fill in the deployment form:

```
Repository: Kiranrossi/Enterprise-Documentation-Q-A
Branch: main
Main file path: app.py
App URL (optional): your-custom-name
```

### Step 4: Advanced Settings (Click "Advanced settings...")

**Python version:** 3.10

**Secrets:** Click "Secrets" and add:

```toml
# Required: Groq API Key
GROQ_API_KEY = "your_actual_groq_api_key_here"

# Required: LLM Configuration
LLM_PROVIDER = "groq"
LLM_MODEL = "llama-3.3-70b-versatile"

# Optional: If using cloud-hosted Endee
# ENDEE_BASE_URL = "http://your-endee-server:8080/api/v1"
# ENDEE_AUTH_TOKEN = "your_token_if_needed"

# Optional: For local Endee (won't work on Streamlit Cloud)
ENDEE_HOST = "localhost"
ENDEE_PORT = "8080"
```

### Step 5: Deploy!

Click **"Deploy!"** button

---

## ⏱️ Wait for Build

- Build time: ~2-3 minutes
- Watch the logs for any errors
- App will auto-open when ready

---

## 🧪 Test Your Deployment

### 1. Check UI Loads
- [ ] App loads without errors
- [ ] Sidebar shows Groq API configured
- [ ] No connection errors in logs

### 2. Upload Document
- [ ] Upload a PDF/TXT file
- [ ] Click "Index Documents"
- [ ] Check for success message

### 3. Ask Question
- [ ] Enter a question
- [ ] Click "Ask"
- [ ] Verify answer is generated
- [ ] Check source citations

---

## ⚠️ Important Notes

### Endee Requirement

**This app requires Endee Vector Database to function fully.**

Since Streamlit Cloud doesn't support Docker, you have 3 options:

#### Option 1: Local Demo (Easiest for Testing)
- Run locally: `streamlit run app.py`
- Share via ngrok or similar

#### Option 2: Cloud-Hosted Endee (Production)
- Deploy Endee on DigitalOcean/AWS/Railway
- Add `ENDEE_BASE_URL` to Streamlit secrets
- See `DEPLOYMENT.md` for details

#### Option 3: Mock Mode (Demo Only)
- App will show error when trying to index
- Good for showcasing UI only

---

## 🔧 Troubleshooting

### Build Fails

**Check:**
- All dependencies in `requirements.txt`
- Python version compatibility
- No syntax errors in code

**View logs:**
- Click "Manage app" → "Logs"

### Runtime Errors

**Common issues:**

1. **"Groq API Error"**
   - Check API key in secrets
   - Verify key is valid at console.groq.com

2. **"Endee Connection Error"**
   - Normal if using localhost (won't work on cloud)
   - Deploy Endee separately or run locally

3. **"Module not found"**
   - Ensure package in requirements.txt
   - Check package name spelling

---

## 📊 Monitor Your App

### Streamlit Cloud Dashboard

- **Logs**: Real-time application logs
- **Analytics**: Usage statistics
- **Settings**: Update secrets, reboot app

### Useful Commands

```bash
# View app logs
# (Available in Streamlit Cloud dashboard)

# Reboot app
# Click "Reboot app" in dashboard

# Update code
git push origin main  # Auto-deploys
```

---

## 🎯 Post-Deployment

### Share Your App

Your app URL:
```
https://your-app-name.streamlit.app
```

### Optional: Custom Domain

1. Go to app settings
2. Click "Custom domain"
3. Follow DNS configuration steps

### Monitor Usage

- Check Groq API usage: console.groq.com
- Monitor Streamlit analytics
- Review error logs regularly

---

## 💡 Tips for Success

1. **Start Simple**: Test with small documents first
2. **Monitor Costs**: Watch Groq API usage
3. **Optimize Performance**: Adjust chunk size if needed
4. **User Feedback**: Collect feedback and iterate
5. **Documentation**: Share README with users

---

## 🆘 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: [Your repo issues](https://github.com/Kiranrossi/Enterprise-Documentation-Q-A/issues)

---

## ✨ You're All Set!

Your Enterprise RAG System is now live! 🎉

**Next steps:**
1. Share the URL with your team
2. Upload your documentation
3. Start asking questions!

---

**Happy Deploying! 🚀**
