import os
import pathway as pw
from pathway.xpacks.llm import embedders, llms
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration values (Gemini specifics)
embedder_locator = os.environ.get("EMBEDDER_LOCATOR", "avsolatorio/GIST-small-Embedding-v0")
api_key = os.environ.get("GEMINI_API_TOKEN", "")
model_locator = os.environ.get("MODEL_LOCATOR", "gemini-lite")
max_tokens = int(os.environ.get("MAX_TOKENS", 200))
temperature = float(os.environ.get("TEMPERATURE", 0.0))


def gemini_embedder(data):
    # Using SentenceTransformerEmbedder from Pathway's LLM module
    embedder = embedders.SentenceTransformerEmbedder(
        embedder_locator,
        call_kwargs={"show_progress_bar": False}
    )
    # Apply the embedding to the input data
    return embedder.apply(text=data)


def gemini_chat_completion(prompt):
    # Using LiteLLMChat from Pathway's LLM module
    model = llms.LiteLLMChat(
        model=model_locator,
        retry_strategy=pw.udfs.ExponentialBackoffRetryStrategy(max_retries=6),
        cache_strategy=pw.udfs.DiskCache()
    )
    
    return model.apply(
        prompt,
        locator=model_locator,
        temperature=temperature,
        max_tokens=max_tokens,
    )

# Example usage
# if __name__ == "__main__":
    # sample_prompt = "What is the capital of France?"
    # print(gemini_chat_completion(sample_prompt))
