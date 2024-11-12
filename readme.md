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
