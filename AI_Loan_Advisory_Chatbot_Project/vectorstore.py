import cohere
from pinecone import Pinecone, ServerlessSpec
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time

def load_loan_document(file_path="loan_data.txt"):
    """Load loan advisory document from text file"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def split_text_into_chunks(text):
    """Split text into smaller chunks for better retrieval"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "?", "!", " "]
    )
    chunks = splitter.split_text(text)
    # Filter out very short chunks
    chunks = [c.strip() for c in chunks if len(c.strip()) > 50]
    return chunks

def create_embeddings(chunks, cohere_api_key):
    """Convert text chunks into vector embeddings using Cohere"""
    co = cohere.ClientV2(cohere_api_key)
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"]
    )
    return response.embeddings.float

def store_in_pinecone(chunks, embeddings, pinecone_api_key,
                      index_name="loan-advisory"):
    """Store embeddings in Pinecone vector database"""
    pc = Pinecone(api_key=pinecone_api_key)

    # Delete old index if exists and recreate
    existing = [idx.name for idx in pc.list_indexes()]
    if index_name in existing:
        pc.delete_index(index_name)
        time.sleep(3)

    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

    # Wait for index to be ready
    time.sleep(5)
    index = pc.Index(index_name)

    # Upsert in batches of 50
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        batch_embeddings = embeddings[i:i+batch_size]
        vectors = [
            {
                "id": f"chunk-{i+j}",
                "values": emb,
                "metadata": {"text": chunk}
            }
            for j, (chunk, emb) in enumerate(zip(batch_chunks, batch_embeddings))
        ]
        index.upsert(vectors=vectors)

    print(f"Stored {len(chunks)} chunks in Pinecone.")
    return index

def retrieve_relevant_chunks(query, cohere_api_key, pinecone_api_key,
                              index_name="loan-advisory", top_k=5):
    """Retrieve top-k relevant chunks for a user query"""
    co = cohere.ClientV2(cohere_api_key)
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(index_name)

    # Embed the query
    query_embedding = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query",
        embedding_types=["float"]
    ).embeddings.float[0]

    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    context_chunks = [
        match["metadata"]["text"]
        for match in results["matches"]
        if match["score"] > 0.3
    ]
    return context_chunks
