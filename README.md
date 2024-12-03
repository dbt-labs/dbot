# ***Archival Notice***
This repository has been archived.

As a result all of its historical issues and PRs have been closed.

Please *do not clone* this repo without understanding the risk in doing so:
- It may have unaddressed security vulnerabilities
- It may have unaddressed bugs

<details>
   <summary>Click for historical readme</summary>

# dbot
An LLM-powered chatbot with the added context of the dbt knowledge base.

## An experiment
This is currently a basic CLI prototype that has been supplied with the knowledge of the dbt Developer Hub (docs, guides, etc) and uses this to add context to questions asked by users.

## How does it work?
It stores embeddings of the material on the Developer Hub (chunked by markdown heading sections) in a vector database, and finds documents similar to the question that is asked. It then prepends as much of that context onto the prompt as it can fit in ChatGPT's context window.

