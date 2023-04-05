# dbot
An LLM-powered chatbot with the added context of the dbt knowledge base.

## An experiment
This is currently a basic CLI prototype that has been supplied with the knowledge of the dbt Developer Hub (docs, guides, etc) and uses this to add context to questions asked by users.

## How does it work?
It stores embeddings of the material on the Developer Hub (chunked by markdown heading sections) in a vector database, and finds documents similar to the question that is asked. It then prepends as much of that context onto the prompt as it can fit in ChatGPT's context window.
