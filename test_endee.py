#!/usr/bin/env python3
"""Test script to verify Endee indexing and retrieval works."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.vector_store import EndeeClient, VectorIndexer, VectorRetriever
from src.embeddings import EmbeddingModel
from src.utils import log

def test_endee_flow():
    """Test the complete Endee indexing and retrieval flow."""
    
    print("\n" + "="*60)
    print("Testing Endee RAG Flow")
    print("="*60 + "\n")
    
    # Step 1: Create client
    print("1. Creating Endee client...")
    client = EndeeClient()
    print("   ✅ Client created\n")
    
    # Step 2: Delete existing index
    print("2. Deleting existing index (if any)...")
    if client.index_exists('technical_docs'):
        client.delete_index('technical_docs')
        print("   ✅ Deleted old index")
    else:
        print("   ℹ️  No existing index")
    print()
    
    # Step 3: Create test data
    print("3. Creating test data...")
    test_chunks = [
        {
            "text": "The internship duration is 6 months starting from January 2024.",
            "source": "test_doc.pdf",
            "filename": "test_doc.pdf",
            "chunk_id": 0
        },
        {
            "text": "The monthly stipend is $2000 for the internship program.",
            "source": "test_doc.pdf",
            "filename": "test_doc.pdf",
            "chunk_id": 1
        }
    ]
    print(f"   ✅ Created {len(test_chunks)} test chunks\n")
    
    # Step 4: Generate embeddings
    print("4. Generating embeddings...")
    embedding_model = EmbeddingModel()
    texts = [chunk['text'] for chunk in test_chunks]
    embeddings = embedding_model.encode_batch(texts)
    print(f"   ✅ Generated {len(embeddings)} embeddings\n")
    
    # Step 5: Index in Endee
    print("5. Indexing in Endee...")
    indexer = VectorIndexer(client)
    indexer.setup_index(force_recreate=True)
    num_indexed = indexer.upsert_chunks(test_chunks, embeddings)
    print(f"   ✅ Indexed {num_indexed} chunks\n")
    
    # Step 6: Verify index exists
    print("6. Verifying index...")
    if client.index_exists('technical_docs'):
        print("   ✅ Index exists")
    else:
        print("   ❌ Index does NOT exist!")
        return False
    print()
    
    # Step 7: Create retriever
    print("7. Creating retriever...")
    retriever = VectorRetriever(client)
    if retriever.index:
        print("   ✅ Retriever has index reference")
    else:
        print("   ❌ Retriever does NOT have index reference!")
        return False
    print()
    
    # Step 8: Test query
    print("8. Testing query...")
    query_text = "What is the duration?"
    query_embedding = embedding_model.encode(query_text)[0]  # Get first (and only) embedding
    results = retriever.search(query_embedding, top_k=2)
    print(f"   ✅ Found {len(results)} results")
    
    if results:
        print("\n   Top result:")
        print(f"   - Text: {results[0].get('meta', {}).get('text', 'N/A')[:80]}...")
        print(f"   - Similarity: {results[0].get('similarity', 0):.3f}")
    print()
    
    print("="*60)
    if len(results) > 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ TESTS FAILED - No results found")
    print("="*60 + "\n")
    
    return len(results) > 0

if __name__ == "__main__":
    success = test_endee_flow()
    sys.exit(0 if success else 1)
