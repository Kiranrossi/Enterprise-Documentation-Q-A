# 🔑 API Keys Setup Guide

## Required API Keys

This project requires **one API key** to function:

### 1. OpenAI API Key (Required)

**Purpose**: Used for generating answers with GPT models

**How to get it**:

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the key (starts with `sk-...`)
6. **Important**: Save it immediately - you won't see it again!

**Cost**: 
- Pay-as-you-go pricing
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens
- Typical query: ~$0.001-0.005

---

## How to Add Your API Key

### Method 1: Edit .env File (Recommended)

1. Open the `.env` file in your project root:
   ```bash
   nano .env
   # or use any text editor
   ```

2. Find this line:
   ```
   OPENAI_API_KEY=
   ```

3. Add your API key after the `=`:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. Save the file

### Method 2: Via Streamlit UI (Temporary)

You can also enter your API key directly in the Streamlit sidebar when running the app. However, this is temporary and you'll need to re-enter it each time.

---

## Verifying Your Setup

### Check .env File

```bash
cat .env | grep OPENAI_API_KEY
```

Should show:
```
OPENAI_API_KEY=sk-...your-key...
```

### Test the Application

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. If the API key is valid:
   - ✅ No errors when asking questions
   - ✅ Answers are generated successfully

3. If the API key is invalid:
   - ❌ "Invalid API key" error
   - ❌ "Incorrect API key provided" message

---

## Alternative: Use Open-Source LLMs (No API Key Needed)

If you don't want to use OpenAI, you can use **free, open-source models**:

### Option 1: Hugging Face Inference API

1. Get a free API key from [Hugging Face](https://huggingface.co/settings/tokens)

2. Update `.env`:
   ```bash
   HUGGINGFACE_API_KEY=hf_your_key_here
   LLM_PROVIDER=huggingface
   LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
   ```

3. Modify `src/generation/llm_client.py` to support Hugging Face (requires code changes)

### Option 2: Local LLM (Ollama)

1. Install [Ollama](https://ollama.ai/)
2. Run a local model:
   ```bash
   ollama run llama2
   ```
3. Modify the LLM client to use Ollama API (requires code changes)

---

## Security Best Practices

### ✅ DO:
- Keep `.env` file private (already in `.gitignore`)
- Never commit API keys to Git
- Use environment variables for secrets
- Rotate keys periodically

### ❌ DON'T:
- Share your `.env` file
- Commit `.env` to GitHub
- Hardcode API keys in code
- Share API keys in screenshots

---

## Troubleshooting

### "No API key provided"

**Solution**: 
- Check `.env` file exists
- Verify `OPENAI_API_KEY=` has a value
- Restart the Streamlit app

### "Incorrect API key provided"

**Solution**:
- Verify the key is correct (starts with `sk-`)
- Check for extra spaces or quotes
- Generate a new key from OpenAI dashboard

### "You exceeded your current quota"

**Solution**:
- Add billing information to your OpenAI account
- Check your usage limits
- Upgrade your plan if needed

### "Rate limit exceeded"

**Solution**:
- Wait a few seconds and try again
- Reduce the number of requests
- Upgrade to a higher tier plan

---

## Cost Estimation

### Typical Usage:

**Indexing 100 documents**:
- Embedding: FREE (local Sentence-BERT model)
- Vector storage: FREE (self-hosted Endee)
- Total: $0

**Asking 100 questions**:
- Retrieval: FREE (Endee)
- LLM generation: ~$0.10-0.50 (depending on model)
- Total: ~$0.10-0.50

**Monthly estimate** (moderate use):
- ~500 questions/month
- Cost: ~$0.50-2.50/month

---

## Quick Setup Checklist

- [ ] Get OpenAI API key from platform.openai.com
- [ ] Open `.env` file
- [ ] Add API key: `OPENAI_API_KEY=sk-...`
- [ ] Save the file
- [ ] Run `streamlit run app.py`
- [ ] Test with a question
- [ ] ✅ Success!

---

## Need Help?

If you're having issues with API keys:

1. Check the [OpenAI API documentation](https://platform.openai.com/docs/api-reference)
2. Verify your billing is set up
3. Check the error messages in the Streamlit app
4. Review logs in `logs/` directory

---

**Remember**: The `.env` file is already in `.gitignore`, so your API keys won't be committed to Git! 🔒
