Google converts text to numbers

Pinecone stores and searches those numbers

result = client.models.embed_content(
    model="models/text-embedding-004",
    contents=[query]
)
query_vector = result.embeddings[0].values

Takes your question ("What is my academic focus?")
Converts it to a vector (list of 768 numbers that represent the meaning)

Search Pinecone

Searches the database by comparing your query vector to all stored vectors
Finds the most similar memory using mathematical distance (cosine similarity)
top_k=1 means "give me just the single best match"

If a match is found, shows:
Confidence score: How similar the meanings are (0.0 = not related, 1.0 = identical)
The fact: The original text that was stored

Why This Works:
Traditional Search:

Query: "What is my academic focus?"
Only finds exact words like "academic" or "focus"
Vector Search (This Script):

Query: "What is my academic focus?"
Finds similar meanings like "I study computer science" or "My major is engineering"
Works because similar meanings = similar vectors