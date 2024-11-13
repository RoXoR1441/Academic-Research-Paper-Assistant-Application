# Research Paper Assistant

A Python-based Research Paper Assistant application that helps users store, query, and summarize academic research papers, along with generating future research directions. The application utilizes Neo4j for storing paper metadata and content and Ollama’s LLM API for handling natural language queries.

## Features

- **PDF Text Extraction**: Extracts text content from PDF research papers.
- **Neo4j Database Integration**: Stores research papers in a Neo4j graph database.
- **Interactive Chatbot**: Provides a chatbot interface to answer questions about papers, summarize content, and suggest future research directions.
- **Natural Language Processing with Ollama API**: Uses the Ollama API for generating responses to user queries.

## Prerequisites

- **Python** 3.8+
- **Neo4j** (Community or Enterprise Edition)
- **Ollama API** running locally
- Python libraries:
  - `requests`
  - `fitz` (PyMuPDF for PDF processing)
  - `neo4j`

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/RoXoR1441/research-paper-assistant.git
   cd research-paper-assistant

## Working of code

This code is designed to build a research paper assistant that processes academic papers, stores their information in a Neo4j graph database, and provides an interactive chatbot for querying the papers. First, it establishes a connection to a Neo4j database, where the paper details will be stored. The Neo4j database helps organize and query the papers based on their titles, content, and publication dates.

Next, the code interacts with the Ollama API, which is used to generate responses for specific queries about the papers. The Ollama model processes natural language prompts, allowing the assistant to summarize the contents of papers or suggest future work based on them. These responses are tailored to the user’s request, such as summarizing advancements or recommending future research directions.

The code also includes functionality to process PDF research papers. It extracts the text from each PDF file in a specified folder and stores the relevant metadata (such as title, content, and publication date) in the Neo4j database. The database stores each paper as a node with properties like title and content, making it easy to query the papers later.

Finally, a chatbot interface is implemented where the user can input queries. The chatbot communicates with the Ollama API to provide answers to the user’s questions. If a user asks for a summary or future work suggestions, the assistant generates appropriate responses. The user can also ask general questions about the papers, and the chatbot will retrieve and present the relevant information. The program processes the papers in a given folder, stores them in the database, and then starts the chatbot interface for user interaction.
