# backend/test_embeddings.py
import os
import time

# Set the environment variable like we did in the .env file
# This is to ensure our test is consistent.
os.environ["TOKENIZERS_PARALLELISM"] = "false"

print("Attempting to import HuggingFaceEmbeddings...")
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("Import successful!")
except Exception as e:
    print(f"Failed to import HuggingFaceEmbeddings: {e}")
    exit()

try:
    print("\nLoading the embedding model...")
    print("(This may take a moment as it downloads or loads the model into memory...)")

    start_time = time.time()
    # Initialize the model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    end_time = time.time()

    print(f"\nModel loaded successfully in {end_time - start_time:.2f} seconds.")

    print("\nAttempting to create an embedding for a test sentence...")
    test_vector = embeddings.embed_query("This is a test sentence.")
    print("Successfully created a test embedding!")
    print("Embedding dimensions:", len(test_vector))

except Exception as e:
    print(f"\n--- An Error Occurred ---")
    print(f"Error: {e}")