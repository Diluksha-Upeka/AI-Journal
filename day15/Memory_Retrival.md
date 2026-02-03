# Memory Retrieval System

## Architecture

**Google AI** → Converts text to 768-dimensional vectors  
**Pinecone** → Stores and searches vectors using cosine similarity

---

## How It Works

### 1. Query Embedding
```python
result = client.models.embed_content(
    model="models/text-embedding-004",
    contents=[query]
)
query_vector = result.embeddings[0].values
```
Transforms your question into a 768-number vector representing semantic meaning.

### 2. Vector Search
```python
search_results = index.query(
    vector=query_vector,
    top_k=1,
    include_metadata=True
)
```
- Compares query vector against all stored vectors
- Returns closest match by cosine similarity
- `top_k=1` retrieves single best result

### 3. Result
- **Score**: 0.0 (unrelated) → 1.0 (identical)
- **Text**: Original stored fact

---

## Semantic vs Keyword Search

| Traditional Search | Vector Search |
|-------------------|---------------|
| "academic focus" → Matches exact words | "academic focus" → Finds "study CS", "engineering major", etc. |
| Brittle, literal | Understands meaning |

**Key Insight**: Similar meanings produce similar vectors, enabling semantic discovery beyond exact matches.