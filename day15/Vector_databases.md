# The Embedder
*How text becomes numbers - RAG*

## Embedding
A sentence → long list of numbers (vector)

## Vector Space
- Each number represents a dimension
- Each sentence is a point in that space
- **Distance = meaning difference**
    - Closer points = similar meaning
    - Farther points = different meaning

## Vector Databases
- Store vectors efficiently
- Enable fast similarity searches
- Essential for RAG (Retrieval-Augmented Generation)

## Why 768 Numbers?
Common embedding dimension size that balances detail and computational efficiency

## How It Works
```
Text Input 
    → Embedder Model (Google Gemini, OpenAI, etc.)
    → Number Vector (768 dimensions)
    → Vector Database (Pinecone, Weaviate, etc.)
```