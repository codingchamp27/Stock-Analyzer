import os
import pathway as pw
from pathway.xpacks.llm import embedders
from pathway.stdlib.ml.index import KNNIndex
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

embedding_dimension = int(os.environ.get("EMBEDDING_DIMENSION", 768))  # Adjusted embedding dimension for Gemini
embedder_locator = os.environ.get("EMBEDDER_LOCATOR", "avsolatorio/GIST-small-Embedding-v0")


def embeddings(context, data_to_embed):
    # Use Pathway's SentenceTransformerEmbedder instead of custom gemini_embedder
    embedder = embedders.SentenceTransformerEmbedder(
        embedder_locator,
        call_kwargs={"show_progress_bar": False}
    )
    
    # Apply the embedding to the input data
    embedded_data = embedder.apply(text=data_to_embed)
    
    # Return the context with the added vector embeddings
    return context + context.select(vector=embedded_data)


def index_embeddings(embedded_data):
    # Use the Pathway KNNIndex for indexing the embeddings
    return KNNIndex(embedded_data.vector, embedded_data, n_dimensions=embedding_dimension)
