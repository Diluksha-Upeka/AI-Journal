import os
import google.genai
from pinecone import Pinecone
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import time

load_dotenv()

# Setup Google (The Embedder)
client = google.genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("memory-index") 

# This script reads a PDF, chunks the text, embeds it, and stores it in Pinecone for later retrieval by the RAG agent.
def ingest_file(file_path):
    print(f"Opening file: {file_path}")

    # 1. Read the PDF
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    print(f"Read {len(text)} characters from the PDF.")

    # 2. Chunk the text into smaller pieces
    # chunk_size = 500 : Each piece is ~1 paragraph
    # chunk_overlap = 50 : We want some overlap to maintain context between chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    print(f"Split text into {len(chunks)} chunks.")

    # 3. Embed each chunk and store in Pinecone
    print("Embedding and storing chunks in Pinecone...")

    for i, chunk in enumerate(chunks):
        # Create a unique ID for each chunk (e.g., using the file name and chunk index)
        chunk_id = f"pdf_chunk_{i}"

        # Get vector embedding for the chunk
        try:
            vector = client.models.embed_content(
                model="models/text-embedding-004",
                contents=[chunk]
            ).embeddings[0].values

            # Upload
            index.upsert(
                vectors=[{
                    "id": chunk_id,
                    "values": vector,
                    "metadata": {"text": chunk}
                }]
            )

            # Sleep to avoid rate limits
            time.sleep(1)

            # Print progress every 1 chunk
            if i % 1 == 0:
                print(f"Processed {i}/{len(chunks)} chunks...")

        except Exception as e:
            print(f"Error processing chunk {i}: {e}")
    print("Finished ingesting file.")

if __name__ == "__main__":
    ingest_file("sample.pdf")