import pathway as pw
from datetime import datetime
from pathway.xpacks.llm import llms  # Use Pathway's built-in LLM chat
from pathway.udfs import DiskCache, ExponentialBackoffRetryStrategy

# Function for prompting and returning a response using Pathway
def prompt(index, embedded_query, user_query):

    # Define a UDF to construct the prompt from the local indexed data
    @pw.udf
    def build_prompt(local_indexed_data, query):
        docs_str = "\n".join(local_indexed_data)
        prompt = f"Given the following data: \n{docs_str} \nanswer this query: {query}. Assume that current date is: {datetime.now()}. Please clean and summarize the output."
        return prompt

    # Retrieve the most relevant documents based on the query
    query_context = embedded_query + index.get_nearest_items(
        embedded_query.vector, k=3, collapse_rows=True
    ).select(local_indexed_data_list=pw.this.doc).promise_universe_is_equal_to(embedded_query)

    # Build the prompt using the local indexed data and the user query
    constructed_prompt = query_context.select(
        prompt=build_prompt(pw.this.local_indexed_data_list, user_query)
    )

    # Create a LiteLLMChat model with a retry and cache strategy (using Pathway)
    model = llms.LiteLLMChat(
        model="gemini-lite",  # Assuming gemini-lite is available in Pathway
        retry_strategy=ExponentialBackoffRetryStrategy(max_retries=6),
        cache_strategy=DiskCache(),
    )

    # Return the result of the chat model applied to the constructed prompt
    return constructed_prompt.select(
        query_id=pw.this.id,
        result=model.apply(pw.this.prompt),  # Using Pathway's LiteLLMChat to generate the result
    )

