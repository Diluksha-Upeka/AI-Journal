import os
import time
from dotenv import load_dotenv
import google.genai
from pinecone import Pinecone

# 1. Load Keys
load_dotenv()

# 2. Setup Google (The Embedder)
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")

# 3. Setup Pinecone (The Database)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("memory-index")  # The name of the Pinecone index

def get_embedding(text):
    """Turns text into a list of 768 numbers"""
    # We use the specific embedding model from Google
    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[text]
    )
    return result.embeddings[0].values

def store_fact(fact_id, text):
    """Uploads the text + numbers to the database"""
    print(f"Processing: '{text}'...")
    
    # A. Get numbers
    vector = get_embedding(text)    # List of 768 numbers
    
    # B. Upload to Pinecone
    # Structure: (ID, Vector List, Metadata)
    index.upsert(
        vectors=[
            {
                "id": fact_id, 
                "values": vector, 
                "metadata": {"text": text} # We store the original text so we can read it back later
            }
        ]
    )
    print("Stored successfully!")


if __name__ == "__main__":
    # Let's teach the AI some facts about YOU
    facts = [
        ("fact-1", "The user is a Computer Engineering student at UoR."),
        ("fact-2", "The user loves Computer Vision and Image Processing."),
        ("fact-3", "The user hates fixing CSS bugs.")
    ]
    
    for ids, text in facts:
        store_fact(ids, text)
        time.sleep(1) # To avoid rate limiting issues