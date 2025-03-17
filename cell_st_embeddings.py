
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load dataset with expanded interests
books_df = pd.read_pickle("books_with_expanded_interest.pkl")

# Load SentenceTransformer model
st_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_st_embedding(text):
    return st_model.encode(text).astype("float32")

# Compute embeddings
books_df["st_embedding"] = books_df["expanded_interest"].apply(lambda x: get_st_embedding(x).tolist())

# Convert to NumPy matrix
st_matrix = np.array(books_df["st_embedding"].tolist()).astype("float32")
np.save("st_embeddings.npy", st_matrix)  

# Create FAISS index
faiss.normalize_L2(st_matrix)
index_st = faiss.IndexFlatL2(st_matrix.shape[1])
index_st.add(st_matrix)

faiss.write_index(index_st, "faiss_st.index")

print("✅ SentenceTransformer embeddings computed and saved in faiss_st.index and stored embeddings for dataset books st_embeddings.npy.")
