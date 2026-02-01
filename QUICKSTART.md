# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Setup Environment (1 minute)

```bash
# Run the automated setup script
./setup.sh
```

This will:
- Start Endee vector database via Docker
- Create .env file
- Install Python dependencies

### Step 2: Configure API Key (30 seconds)

Edit `.env` and add your OpenAI API key:

```bash
# Open .env file
nano .env  # or use your favorite editor

# Add your API key
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 3: Run the Application (30 seconds)

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 4: Test with Sample Data (3 minutes)

1. **Enter API Key**: In the sidebar, paste your OpenAI API key
2. **Upload Sample Document**: 
   - Click "Browse files" in the sidebar
   - Select `data/raw/sample_api_docs.md`
3. **Index the Document**: Click "🔄 Index Documents"
4. **Ask a Question**: Try these example questions:
   - "How does authentication work in this API?"
   - "What happens when a request times out?"
   - "What are the limitations of batch ingestion?"
5. **View Results**: See the answer, sources, and similarity scores!

---

## 📝 Example Questions to Try

### Authentication
- "How do I authenticate with the API?"
- "What OAuth flows are supported?"
- "How do I use the access token?"

### Error Handling
- "What happens when a request times out?"
- "How should I implement retry logic?"
- "What error codes does the API return?"

### Vector Indexing
- "How does vector indexing work?"
- "What distance metrics are supported?"
- "How do I create an index?"

### Batch Operations
- "What are the limitations of batch ingestion?"
- "What is the maximum batch size?"
- "What are the best practices for batch processing?"

---

## 🔍 Verifying Everything Works

### Check Endee is Running

```bash
docker ps
# Should show: endee-server running on port 8080
```

### Check Endee Health

```bash
curl http://localhost:8080/health
# Should return: {"status": "ok"}
```

### View Endee Logs

```bash
docker logs endee-server
```

---

## 🐛 Common Issues

### "Could not connect to Endee"

**Solution:**
```bash
# Restart Endee
docker compose restart

# Or start fresh
docker compose down
docker compose up -d
```

### "No module named 'endee'"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Invalid API key"

**Solution:**
- Check your OpenAI API key is correct
- Ensure you have billing enabled
- Verify the key has not expired

---

## 📊 What to Expect

### After Indexing
- ✅ "Indexed X chunks in Endee" message
- ✅ Green "Documents Indexed" status in sidebar

### After Asking a Question
- ✅ Generated answer (2-3 seconds)
- ✅ Source documents with similarity scores
- ✅ Confidence metrics

### Performance
- **Indexing**: ~10-20 seconds for sample document
- **Query**: ~2-3 seconds per question
- **Accuracy**: High relevance for technical questions

---

## 🎯 Next Steps

1. **Upload Your Own Documents**:
   - PDF, TXT, MD, or DOCX files
   - Technical documentation works best
   
2. **Experiment with Settings**:
   - Adjust "Number of context chunks" (top_k)
   - Try different temperature values
   - Set minimum similarity threshold

3. **Deploy to Streamlit Cloud**:
   - Push to GitHub
   - Connect to Streamlit Cloud
   - Add API key in secrets
   - Share with your team!

---

## 📚 Additional Resources

- **Full Documentation**: See [README.md](README.md)
- **Architecture Details**: See [PROJECT_PLAN.md](PROJECT_PLAN.md)
- **Progress Tracker**: See [PROGRESS.md](PROGRESS.md)
- **Endee Docs**: https://docs.endee.io

---

**Happy querying! 🎉**
