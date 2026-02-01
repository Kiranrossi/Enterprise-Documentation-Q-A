"""Streamlit application for RAG-powered documentation Q&A."""

import streamlit as st
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import settings, log
from src.ingestion import DocumentLoader, TextCleaner, TextChunker
from src.embeddings import EmbeddingModel
from src.vector_store import EndeeClient, VectorIndexer, VectorRetriever
from src.generation import RAGGenerator

# Page configuration
st.set_page_config(
    page_title=settings.app_title,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_generator' not in st.session_state:
    st.session_state.rag_generator = None
if 'indexed' not in st.session_state:
    st.session_state.indexed = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_system():
    """Initialize RAG system components."""
    try:
        with st.spinner("Initializing RAG system..."):
            # Check if Endee is accessible
            try:
                client = EndeeClient()
                st.success("✅ Connected to Endee vector database")
            except Exception as e:
                st.error(f"❌ Could not connect to Endee: {e}")
                st.info("Please ensure Endee is running: `docker compose up -d`")
                return False
            
            # Initialize components
            embedding_model = EmbeddingModel()
            retriever = VectorRetriever(client)
            rag_generator = RAGGenerator(
                embedding_model=embedding_model,
                retriever=retriever
            )
            
            st.session_state.rag_generator = rag_generator
            st.success("✅ RAG system initialized successfully")
            return True
            
    except Exception as e:
        st.error(f"Error initializing system: {e}")
        return False

def index_documents(uploaded_files):
    """Index uploaded documents."""
    if not uploaded_files:
        st.warning("Please upload documents first")
        return False
    
    try:
        with st.spinner("Processing and indexing documents..."):
            # Save uploaded files
            data_dir = settings.raw_data_dir
            saved_files = []
            
            for uploaded_file in uploaded_files:
                file_path = data_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                saved_files.append(file_path)
            
            st.info(f"Saved {len(saved_files)} files")
            
            # Load documents
            loader = DocumentLoader()
            documents = []
            for file_path in saved_files:
                doc = loader.load_file(file_path)
                if doc:
                    documents.append(doc)
            
            st.info(f"Loaded {len(documents)} documents")
            
            # Clean and chunk
            cleaner = TextCleaner()
            chunker = TextChunker()
            
            all_chunks = []
            for doc in documents:
                cleaned_text = cleaner.preprocess(doc['text'])
                doc['text'] = cleaned_text
                chunks = chunker.chunk_document(doc, strategy="tokens")
                all_chunks.extend(chunks)
            
            st.info(f"Created {len(all_chunks)} chunks")
            
            # Generate embeddings
            embedding_model = EmbeddingModel()
            texts = [chunk['text'] for chunk in all_chunks]
            embeddings = embedding_model.encode_batch(texts, batch_size=32)
            
            st.info(f"Generated {len(embeddings)} embeddings")
            
            # Index in Endee
            client = EndeeClient()
            indexer = VectorIndexer(client)
            indexer.setup_index(force_recreate=True)
            num_indexed = indexer.upsert_chunks(all_chunks, embeddings)
            
            st.success(f"✅ Indexed {num_indexed} chunks in Endee")
            st.session_state.indexed = True
            
            # Reinitialize RAG generator so retriever picks up the new index
            embedding_model = EmbeddingModel()
            retriever = VectorRetriever(client)
            st.session_state.rag_generator = RAGGenerator(
                embedding_model=embedding_model,
                retriever=retriever
            )
            st.info("✅ System refreshed - ready to answer questions!")
            
            return True
            
    except Exception as e:
        st.error(f"Error indexing documents: {e}")
        log.error(f"Indexing error: {e}")
        return False

def main():
    """Main application."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Enterprise Documentation Q&A</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">RAG-powered technical documentation assistant using Endee Vector Database</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Show API key status (configured in .env)
        if settings.groq_api_key:
            st.success("✅ Groq API Key: Configured")
        else:
            st.error("❌ Groq API Key: Not configured in .env")
        
        st.divider()
        
        # Document upload
        st.header("📄 Document Management")
        uploaded_files = st.file_uploader(
            "Upload Documentation",
            type=['pdf', 'txt', 'md', 'docx'],
            accept_multiple_files=True,
            help="Upload technical documentation files"
        )
        
        if st.button("🔄 Index Documents", use_container_width=True):
            if uploaded_files:
                index_documents(uploaded_files)
            else:
                st.warning("Please upload files first")
        
        st.divider()
        
        # Settings
        st.header("🎛️ Query Settings")
        top_k = st.slider("Number of context chunks", 1, 10, 5)
        temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.3, 0.1)
        min_similarity = st.slider("Minimum Similarity", 0.0, 1.0, 0.0, 0.05)
        
        st.divider()
        
        # System status
        st.header("📊 System Status")
        if st.session_state.indexed:
            st.success("✅ Documents Indexed")
        else:
            st.info("ℹ️ No documents indexed yet")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["💬 Ask Questions", "📚 About", "🔧 Setup"])
    
    with tab1:
        # Initialize system if not done
        if st.session_state.rag_generator is None:
            if not initialize_system():
                st.stop()
        
        # Check if documents are indexed
        if not st.session_state.indexed:
            st.warning("⚠️ Please upload and index documents first using the sidebar")
            st.stop()
        
        # Query interface
        st.header("Ask a Question")
        
        query = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="e.g., How does authentication work in this API?"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("🔍 Ask", use_container_width=True, type="primary")
        with col2:
            clear_button = st.button("🗑️ Clear History", use_container_width=True)
        
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
        
        if ask_button and query:
            with st.spinner("Generating answer..."):
                result = st.session_state.rag_generator.generate_answer(
                    query=query,
                    top_k=top_k,
                    min_similarity=min_similarity,
                    temperature=temperature
                )
                
                st.session_state.chat_history.append(result)
        
        # Display results
        if st.session_state.chat_history:
            st.divider()
            st.header("💡 Answer")
            
            latest = st.session_state.chat_history[-1]
            
            # Answer
            st.markdown(f"**Question:** {latest['query']}")
            st.markdown(f"**Answer:**\n\n{latest['answer']}")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sources Used", latest['num_sources'])
            with col2:
                st.metric("Top Similarity", f"{latest['top_similarity']:.2%}")
            with col3:
                st.metric("Confidence", "High" if latest['top_similarity'] > 0.7 else "Medium")
            
            # Sources
            if latest['sources']:
                st.divider()
                st.subheader("📖 Sources")
                
                for i, source in enumerate(latest['sources'], 1):
                    with st.expander(f"Source {i}: {source['filename']} (Similarity: {source['similarity']:.2%})"):
                        st.markdown(f"**File:** {source['source']}")
                        st.markdown(f"**Relevance:** {source['similarity']:.2%}")
                        st.markdown(f"**Excerpt:**\n\n{source['text']}")
            
            # Chat history
            if len(st.session_state.chat_history) > 1:
                st.divider()
                st.subheader("📜 Previous Questions")
                
                for i, item in enumerate(reversed(st.session_state.chat_history[:-1]), 1):
                    with st.expander(f"Q{len(st.session_state.chat_history)-i}: {item['query'][:100]}..."):
                        st.markdown(f"**Answer:** {item['answer'][:300]}...")
                        st.markdown(f"**Sources:** {item['num_sources']}")
    
    with tab2:
        st.header("About This System")
        
        st.markdown("""
        ### 🎯 What is this?
        
        This is a **Production-Grade Retrieval-Augmented Generation (RAG) System** for enterprise technical documentation.
        It combines semantic search with large language models to provide accurate, grounded answers to technical questions.
        
        ### 🏗️ Architecture
        
        1. **Document Ingestion**: Load and process technical documentation
        2. **Chunking**: Split documents into semantic chunks
        3. **Embedding**: Convert chunks to vector representations
        4. **Vector Storage**: Store embeddings in Endee vector database
        5. **Retrieval**: Find relevant chunks using semantic search
        6. **Generation**: Generate answers using LLM with retrieved context
        
        ### 🚀 Key Features
        
        - **No Hallucination**: Answers strictly grounded in documentation
        - **Fast Retrieval**: Sub-5ms search latency with Endee
        - **Scalable**: Handles millions of document chunks
        - **Production-Ready**: Enterprise-grade infrastructure
        
        ### 🔧 Technology Stack
        
        - **Vector Database**: Endee.io (high-performance HNSW)
        - **Embeddings**: Sentence-BERT (all-MiniLM-L6-v2)
        - **LLM**: Groq (Llama 3.1 70B)
        - **Framework**: Streamlit
        
        ### 📊 Why Endee?
        
        - **Speed**: 10,000+ QPS, sub-5ms latency
        - **Accuracy**: 99%+ recall
        - **Scale**: Millions of vectors
        - **Cost**: Open-source, self-hosted
        """)
    
    with tab3:
        st.header("Setup Instructions")
        
        st.markdown("""
        ### 📋 Prerequisites
        
        1. **Docker** installed and running
        2. **Python 3.10+**
        3. **Groq API Key** (configured in .env)
        
        ### 🚀 Quick Start
        
        #### 1. Start Endee Vector Database
        
        ```bash
        docker compose up -d
        ```
        
        #### 2. Install Dependencies
        
        ```bash
        pip install -r requirements.txt
        ```
        
        #### 3. Configure Environment
        
        Copy `.env.example` to `.env` and add your Groq API key:
        
        ```bash
        cp .env.example .env
        ```
        
        #### 4. Run the Application
        
        ```bash
        streamlit run app.py
        ```
        
        ### 📝 Usage
        
        1. Upload technical documentation (PDF, TXT, MD, DOCX)
        2. Click "Index Documents"
        3. Ask questions in the main interface

        
        ### 🔍 Example Questions
        
        - "How does authentication work in this API?"
        - "What happens when a request times out?"
        - "How is vector indexing implemented?"
        - "What are the limitations of batch ingestion?"
        
        ### 🐛 Troubleshooting
        
        **Endee Connection Error:**
        - Ensure Docker is running: `docker ps`
        - Check Endee is running: `docker compose ps`
        - Verify port 8080 is available
        
        **Indexing Errors:**
        - Check file formats are supported
        - Ensure files are not corrupted
        - Check logs for detailed errors
        
        **Generation Errors:**
        - Verify Groq API key is valid
        - Check API quota and billing
        - Ensure internet connection
        """)

if __name__ == "__main__":
    main()
