# The embedder
(How text become numbers - RAG)

Embedding 
    A sentence-> long list of numbers (vector)

Vector space
    Each number is a dimension
    Each sentence is a point in that space
    Distance = meaning difference

    closer points = similar meaning
    farther points = different meaning

Vector databases
    Store vectors
    Fast search for similar vectors
    Used in RAG (Retrieval-Augmented Generation)

Why 768 numbers?
    Common size for embeddings
    Balances detail and efficiency

How it works
 Text input -> Embedder model(Google gemini, OpenAI, etc.) -> Number vector (768 dims) -> Store in vector DB (Pinecone, Weaviate, etc.)