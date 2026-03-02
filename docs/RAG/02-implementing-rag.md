# Implementing RAG with Python

This hands-on tutorial walks you through building a complete RAG system from scratch using Python. You will implement every stage of the pipeline: chunking, embedding, vector storage, retrieval, reranking, and generation.

---

## Prerequisites

- Python 3.10+
- A package manager: [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Jupyter Notebook
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) (or any LLM API)

---

## 1. Project Setup

```bash
# Create project directory
mkdir rag-demo && cd rag-demo

# Initialize with uv (or use pip)
uv init .

# Install dependencies
uv add sentence-transformers chromadb google-genai python-dotenv jupyter
```

**What each dependency does:**

| Package | Purpose |
| :--- | :--- |
| `sentence-transformers` | Load embedding models and cross-encoder reranking models |
| `chromadb` | Open-source vector database |
| `google-genai` | Google Gemini API client (free tier available) |
| `python-dotenv` | Load API keys from `.env` files |
| `jupyter` | Interactive notebook environment |

Start Jupyter Notebook with your project dependencies:
```bash
uv run jupyter notebook
```

---

## 2. Step 1 — Chunking

The first step is splitting your document into smaller chunks. Here we use a simple line-based strategy:

```python
from typing import List

def split_into_chunks(doc_path: str) -> List[str]:
    """Read a document and split it into chunks (one per paragraph/line)."""
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by double newlines (paragraphs) and filter empty strings
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks

# Test it
chunks = split_into_chunks("my_document.md")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {chunk[:80]}...")

print(f"\nTotal chunks: {len(chunks)}")
```

### Advanced: Recursive Character Splitting (LangChain Style)

For production systems, use recursive splitting with overlap:

```python
def recursive_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text with overlap to preserve context across boundaries."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # Step back by overlap amount
    return chunks
```

---

## 3. Step 2 — Embedding

Convert each chunk into a vector using a Sentence Transformer embedding model:

```python
from sentence_transformers import SentenceTransformer

# Load an embedding model (downloads ~90MB on first run)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunk(chunk: str) -> List[float]:
    """Convert a text chunk into a vector."""
    vector = embed_model.encode(chunk)
    return vector.tolist()

# Test: embed one chunk
test_vector = embed_chunk(chunks[0])
print(f"Vector dimensions: {len(test_vector)}")
print(f"First 5 values: {test_vector[:5]}")

# Embed ALL chunks
embeddings = [embed_chunk(chunk) for chunk in chunks]
print(f"Total embeddings: {len(embeddings)}")
```

---

## 4. Step 3 — Storing in a Vector Database (ChromaDB)

```python
import chromadb

# Create an in-memory vector database
client = chromadb.EphemeralClient()  
# For persistent storage, use: chromadb.PersistentClient(path="./chroma_db")

# Create a collection (like a "table")
collection = client.create_collection(name="my_documents")

def store_chunks(chunks: List[str], embeddings: List[List[float]]):
    """Store all chunks and their embeddings in ChromaDB."""
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
    print(f"Stored {len(chunks)} chunks in the vector database.")

# Store everything
store_chunks(chunks, embeddings)
```

---

## 5. Step 4 — Retrieval

Search the vector database for chunks most similar to the user's question:

```python
def retrieve(query: str, top_k: int = 5) -> List[str]:
    """Find the top_k most relevant chunks for a given query."""
    query_vector = embed_chunk(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    return results["documents"][0]

# Test retrieval
query = "What are the three secret gadgets Doraemon used?"
retrieved = retrieve(query, top_k=5)

for i, chunk in enumerate(retrieved):
    print(f"\n--- Retrieved Chunk {i+1} ---")
    print(chunk[:200])
```

---

## 6. Step 5 — Reranking with Cross-Encoder

Refine the retrieved results using a more accurate Cross-Encoder model:

```python
from sentence_transformers import CrossEncoder

def rerank(query: str, retrieved_chunks: List[str], top_k: int = 3) -> List[str]:
    """Re-score and re-order retrieved chunks using a Cross-Encoder."""
    # Load cross-encoder model (~400MB on first run)
    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    # Create query-chunk pairs for scoring
    pairs = [[query, chunk] for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)
    
    # Sort by score (descending) and take top_k
    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    return [chunk for chunk, score in scored_chunks[:top_k]]

# Rerank the retrieved results
reranked = rerank(query, retrieved, top_k=3)

for i, chunk in enumerate(reranked):
    print(f"\n--- Reranked Chunk {i+1} ---")
    print(chunk[:200])
```

---

## 7. Step 6 — Generation with an LLM

Finally, send the reranked chunks and the question to a large language model:

```python
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()
google_client = genai.Client()

def generate(query: str, context_chunks: List[str]) -> str:
    """Generate an answer using Gemini based on retrieved context."""
    context = "\n\n".join(context_chunks)
    
    prompt = f"""Based on the following context, answer the user's question.
If the answer cannot be found in the context, say "I don't know based on the provided documents."

Context:
{context}

Question: {query}
"""
    response = google_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

# Generate the final answer!
answer = generate(query, reranked)
print("=" * 60)
print("ANSWER:")
print(answer)
```

### Setting up your `.env` file

Create a `.env` file in your project root:
```text
GEMINI_API_KEY=your_api_key_here
```

---

## 8. Putting It All Together

Here is the complete pipeline in one clean function:

```python
def ask_rag(question: str, doc_path: str = "my_document.md") -> str:
    """End-to-end RAG pipeline: chunk → embed → store → retrieve → rerank → generate."""
    
    # Phase A: Preparation (would normally be done once)
    chunks = split_into_chunks(doc_path)
    embeddings = [embed_chunk(c) for c in chunks]
    store_chunks(chunks, embeddings)
    
    # Phase B: Answering
    retrieved = retrieve(question, top_k=10)
    reranked = rerank(question, retrieved, top_k=3)
    answer = generate(question, reranked)
    
    return answer

# Usage
result = ask_rag("What are the three secret gadgets Doraemon used?")
print(result)
```

---

## 9. Complete Project Structure

```
rag-demo/
├── .env                    # API keys (add to .gitignore!)
├── pyproject.toml          # Dependencies managed by uv
├── my_document.md          # Your knowledge base document
├── rag_notebook.ipynb      # Jupyter notebook with all code
└── chroma_db/              # (Optional) Persistent vector storage
```

---

## Read More

- [Sentence Transformers Documentation](https://www.sbert.net/) — Embedding and cross-encoder model library.
- [ChromaDB Getting Started](https://docs.trychroma.com/getting-started) — Official ChromaDB quickstart guide.
- [Google Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart) — Free LLM API setup.
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/) — Higher-level RAG framework.
- [LlamaIndex Starter Tutorial](https://docs.llamaindex.ai/en/stable/getting_started/starter_example/) — Another popular RAG framework.
- [uv Package Manager](https://docs.astral.sh/uv/) — Fast Python dependency manager used in this tutorial.
- [Pinecone: Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/) — Deep dive into different text splitting approaches.

---

## Knowledge Quiz

**Q1: Why do we use `uv run jupyter notebook` instead of just `jupyter notebook`?**
<details>
<summary>Answer</summary>
Using `uv run` ensures Jupyter launches within the project's virtual environment, so it has access to all the dependencies installed via `uv add`. Running `jupyter notebook` directly would use the system Python, which likely doesn't have `sentence-transformers`, `chromadb`, etc. installed.
</details>

**Q2: What is the purpose of the Cross-Encoder reranking step? Why not just use the embedding similarity directly?**
<details>
<summary>Answer</summary>
Embedding similarity is fast but less accurate — it independently encodes the query and each chunk, then compares their vectors. The Cross-Encoder takes the query and a chunk together as a single input, enabling much deeper semantic comparison. It's slower but significantly more precise, which is why we use it only on the small shortlist (e.g., 10 chunks) returned by retrieval.
</details>

**Q3: What would happen if you used a different embedding model for the query than the one used to embed the document chunks?**
<details>
<summary>Answer</summary>
The retrieval would fail completely. Different embedding models map text into incompatible vector spaces. A query vector from Model A would have no meaningful spatial relationship to chunk vectors from Model B. You MUST use the same embedding model for both indexing and querying.
</details>
