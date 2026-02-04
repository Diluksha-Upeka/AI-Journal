import os
import google.genai
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

# Setup Google (The Embedder)
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("memory-index") 

# Find the correct memory/context from Pinecone
def get_context(query):
    """Searches Pinecone for the most relevant fact"""
    query_vector = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[query]
    ).embeddings[0].values

    results = index.query(
        vector=query_vector,
        top_k=1,
        include_metadata=True
    )

    if results['matches']:
        top_match = results['matches'][0]
        return top_match['metadata']['text']
    return "No relevant context found."

def ask_rag_bot(user_question):
    print(f" Thinking about: '{user_question}'...")
    
    # 1. RETRIEVE (The "Memory" Step) This is memory recall
    context = get_context(user_question)
    print(f" Found Context: {context}")
    
    # 2. AUGMENT (The "Prompt Engineering" Step)
    # We force the AI to use ONLY the context we found.
    prompt = f"""
    You are a helpful assistant. Answer the user's question based ONLY on the context provided below.
    If the context doesn't have the answer, say "I don't know."
    
    Context: {context}
    
    Question: {user_question}
    """
    
    # 3. GENERATE (The "AI" Step)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    print(f"Answer: {response.text}")

if __name__ == "__main__":
    ask_rag_bot("Where does the user study?")