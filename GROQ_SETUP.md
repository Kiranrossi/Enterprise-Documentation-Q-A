# 🚀 Groq API Setup Guide

## Why Groq?

**Groq is PERFECT for this project!** Here's why:

✅ **FREE** - Generous free tier  
✅ **FAST** - Up to 10x faster than OpenAI  
✅ **POWERFUL** - Llama 3.1 70B model  
✅ **EASY** - Simple API, compatible with OpenAI format  

---

## 🔑 Get Your Free Groq API Key (2 minutes)

### Step 1: Sign Up

1. Go to: **https://console.groq.com/**
2. Click **"Sign Up"** or **"Get Started"**
3. Sign up with Google, GitHub, or email

### Step 2: Get API Key

1. After logging in, go to: **https://console.groq.com/keys**
2. Click **"Create API Key"**
3. Give it a name (e.g., "RAG System")
4. Click **"Submit"**
5. **Copy the API key** (starts with `gsk_...`)
6. **Save it immediately** - you won't see it again!

---

## 📝 Add API Key to Your Project

### Method 1: Edit .env File (Recommended)

1. Open `.env` file in your project:
   ```bash
   nano .env
   ```

2. Find this line:
   ```bash
   GROQ_API_KEY=
   ```

3. Paste your API key:
   ```bash
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

4. Save the file (Ctrl+O, Enter, Ctrl+X in nano)

### Method 2: Via Streamlit UI

You can also paste your API key directly in the Streamlit sidebar when running the app.

---

## ✅ Verify Setup

### Check .env File

```bash
cat .env | grep GROQ_API_KEY
```

Should show:
```
GROQ_API_KEY=gsk_...
```

### Test the App

```bash
streamlit run app.py
```

1. Upload a document
2. Index it
3. Ask a question
4. If you see an answer → ✅ **Success!**

---

## 🎯 Available Groq Models

The `.env` file is already configured with the best model, but you can change it:

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `llama-3.1-70b-versatile` | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Recommended** - Best balance |
| `llama-3.1-8b-instant` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Ultra-fast, good quality |
| `mixtral-8x7b-32768` | ⚡⚡⚡ | ⭐⭐⭐⭐ | Long context (32K tokens) |
| `gemma-7b-it` | ⚡⚡⚡⚡ | ⭐⭐⭐ | Lightweight, fast |

To change model, edit `.env`:
```bash
LLM_MODEL=llama-3.1-8b-instant
```

---

## 💰 Pricing (FREE!)

### Free Tier Limits:
- **30 requests per minute**
- **6,000 tokens per minute**
- **14,400 requests per day**

### For This Project:
- **Typical query**: ~500-1000 tokens
- **You can ask**: ~100+ questions per day for FREE!
- **Cost**: $0 🎉

---

## 🆚 Groq vs OpenAI

| Feature | Groq | OpenAI |
|---------|------|--------|
| **Cost** | FREE (generous limits) | $0.002 per 1K tokens |
| **Speed** | 500+ tokens/sec | 50-100 tokens/sec |
| **Model** | Llama 3.1 70B | GPT-3.5-turbo |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Setup** | Easy | Easy |

**Winner for this project**: **Groq** 🏆 (Free + Fast!)

---

## 🐛 Troubleshooting

### "Invalid API key"

**Solution**:
- Check the key starts with `gsk_`
- Verify no extra spaces or quotes
- Generate a new key from console.groq.com

### "Rate limit exceeded"

**Solution**:
- Wait 60 seconds
- You hit the free tier limit (30 req/min)
- Upgrade to paid tier if needed (but free is usually enough!)

### "Model not found"

**Solution**:
- Check model name in `.env` is correct
- Use one of the supported models listed above

---

## 🎓 Quick Start Checklist

- [ ] Go to https://console.groq.com/
- [ ] Sign up (free)
- [ ] Create API key
- [ ] Copy the key (starts with `gsk_`)
- [ ] Open `.env` file
- [ ] Paste key: `GROQ_API_KEY=gsk_...`
- [ ] Save file
- [ ] Run `streamlit run app.py`
- [ ] Test with a question
- [ ] ✅ Success!

---

## 📚 Additional Resources

- **Groq Console**: https://console.groq.com/
- **Groq Documentation**: https://console.groq.com/docs
- **API Reference**: https://console.groq.com/docs/api-reference
- **Playground**: https://console.groq.com/playground

---

## 🎉 You're All Set!

Groq is:
- ✅ Faster than OpenAI
- ✅ Free to use
- ✅ Easy to set up
- ✅ Perfect for RAG systems

**Now go build something amazing!** 🚀
