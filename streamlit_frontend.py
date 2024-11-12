import streamlit as st
import os
from datetime import datetime
from neo4j import GraphDatabase
import fitz  # PyMuPDF for PDF processing
import requests

# Neo4j Setup
uri = "bolt://localhost:7687"  # URI for local Neo4j
username = "neo4j"  # username for Neo4j
password = "12345678"  # Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

# Ollama API setup
ollama_url = "http://127.0.0.1:11434/v1/chat/completions"  # Ollama API endpoint (using 127.0.0.1 for local access)
ollama_model = "llama2" 

# Function to interact with Ollama API
def get_ollama_response(prompt):
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

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to store paper in Neo4j with duplicate check
def store_paper_in_neo4j(title, content, publish_date):
    with driver.session() as session:
        # Check if a paper with the same title already exists
        existing_paper = session.run("MATCH (p:Paper {title: $title}) RETURN p", title=title).single()
        if existing_paper:
            st.warning(f"The paper titled '{title}' already exists in the database.")
        else:
            # If it doesn't exist, store it
            session.run(
                "CREATE (p:Paper {title: $title, content: $content, publish_date: $publish_date})",
                title=title, content=content, publish_date=publish_date
            )
            st.success(f"Paper '{title}' has been successfully stored in the database.")

# Function to list stored papers in Neo4j
def list_papers():
    with driver.session() as session:
        result = session.run("MATCH (p:Paper) RETURN p.title AS title, p.publish_date AS publish_date")
        papers = [{"title": record["title"], "publish_date": record["publish_date"]} for record in result]
        # Remove duplicates by converting to a set of tuples (title, publish_date)
        unique_papers = list({(paper['title'], paper['publish_date']) for paper in papers})
        return [{"title": paper[0], "publish_date": paper[1]} for paper in unique_papers]

# Streamlit UI - Custom CSS Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #FF5F6D, #FFC3A0);  /* Pink to peach gradient */
            font-family: 'Arial', sans-serif;
            color: #333;
        }
        .stButton button {
            background-color: #FF5F6D;  /* Button background color */
            color: white;
            border-radius: 5px;
            font-size: 16px;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #FFC3A0;  /* Button hover color */
        }
        .stTitle {
            color: #FFFFFF;  /* Title color */
            text-align: center;
        }
        .stSubheader {
            color: #F7F7F7;  /* Subheader color */
        }
        .stMarkdown {
            font-size: 18px;  /* Main content text font size */
        }
        .stTextInput input {
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #FF5F6D;
        }
        .stTextInput input:focus {
            border-color: #FFC3A0;
        }
        .stFileUploader input {
            background-color: #FFC3A0;
            padding: 12px;
            border-radius: 10px;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Research Paper Assistant")

# Upload and store papers
st.subheader("Upload Research Papers")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary folder if it doesn't exist
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Save the uploaded file temporarily
    temp_path = os.path.join("temp", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process and store in Neo4j
    paper_content = extract_text_from_pdf(temp_path)
    paper_title = uploaded_file.name
    publish_date = datetime.now().strftime("%Y-%m-%d")
    store_paper_in_neo4j(paper_title, paper_content, publish_date)

# List stored papers
st.subheader("Stored Papers in the Database")
papers = list_papers()
for paper in papers:
    st.write(f"Title: {paper['title']}, Published Date: {paper['publish_date']}")

# Chatbot Interface
st.subheader("Ask the Research Paper Assistant")
query = st.text_input("Enter your question:")
query_type = st.radio("Select query type:", ("Summarize", "Future Work", "General Query"))

if st.button("Get Response"):
    if query_type == "Summarize":
        prompt = f"Summarize the advancements in the following papers: {query}"
    elif query_type == "Future Work":
        prompt = f"Suggest future work based on these papers: {query}"
    else:
        prompt = query
    
    response = get_ollama_response(prompt)
    st.write(f"Response: {response}")
