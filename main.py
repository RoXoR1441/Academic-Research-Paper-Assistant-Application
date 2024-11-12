import os
import requests
import fitz  # PyMuPDF for PDF processing
from datetime import datetime
from neo4j import GraphDatabase

# Neo4j Setup
uri = "bolt://localhost:7687"  # URI for local Neo4j
username = "neo4j"  # username for Neo4j
password = "12345678"  #Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

# Ollama API setup
ollama_url = "http://127.0.0.1:11434/v1/chat/completions"  # Ollama API endpoint (using 127.0.0.1 for local access)
ollama_model = "llama2"  

def get_ollama_response(prompt):
    """Send a prompt to Ollama API and return the response."""
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": ollama_model,
        "temperature": 0.7,
    }
    response = requests.post(ollama_url, json=data, headers=headers)
    response_data = response.json()
    
    if response.status_code == 200:
        return response_data['choices'][0]['message']['content']
    else:
        return "Error: Could not get response from Ollama."

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def store_paper_in_neo4j(title, content, publish_date):
    """Store paper information in Neo4j."""
    with driver.session() as session:
        session.run(
            "CREATE (p:Paper {title: $title, content: $content, publish_date: $publish_date})",
            title=title, content=content, publish_date=publish_date
        )

def start_chatbot():
    """Start the chatbot interface to interact with the user."""
    print("Welcome to the Research Paper Assistant Chatbot!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Handle different types of queries
        if "summarize" in user_input.lower():
            prompt = f"Summarize the advancements in the following papers: {user_input}"
        elif "future work" in user_input.lower():
            prompt = f"Suggest future work based on these papers: {user_input}"
        else:
            prompt = user_input  # General query to answer questions
        
        response = get_ollama_response(prompt)
        print(f"Bot: {response}")

def process_papers(papers_folder):
    """Loop through papers and store them in Neo4j."""
    for filename in os.listdir(papers_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(papers_folder, filename)
            paper_content = extract_text_from_pdf(pdf_path)
            paper_title = filename  
            publish_date = datetime.now().strftime("%Y-%m-%d")  
            store_paper_in_neo4j(paper_title, paper_content, publish_date)

# Main program
if __name__ == "__main__":
    papers_folder = r"C:\Users\dutta\OneDrive\Desktop\attentionAI\papers"  # Folder with PDFs

    # Process all papers in the folder and store them in Neo4j
    process_papers(papers_folder)
    
    # Start the chatbot
    start_chatbot()
