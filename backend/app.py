from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()

def get_chat_response(question, url):
    loader = WebBaseLoader(url)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    embeddings = HuggingFaceEndpointEmbeddings(
        repo_id='sentence-transformers/all-MiniLM-L6-v2',
        task='feature-extraction'
    )
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    retriever = vectorstore.as_retriever()
    
    llm = HuggingFaceEndpoint(
        repo_id='openai/gpt-oss-120b',
        task='text-generation'
    ) # type: ignore
    model = ChatHuggingFace(llm=llm)
    
    prompt = PromptTemplate(
            template=
                    """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.

    Question: {question}

    Context: {context} 

    Answer:
    """,
        input_variables=["question", "context"]
    )
    
    parser = StrOutputParser()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | parser
    )
    
    response = chain.invoke(question)
    return response

# --- Flask App Setup ---
app = Flask(__name__)
# Enable CORS to allow browser extensions or other domains to communicate with this server
CORS(app)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    """
    API endpoint to handle chat requests.
    Expects a JSON payload with 'url' and 'prompt'.
    """
    # Get the JSON data sent from the client
    data = request.get_json()
    
    # Basic validation
    if not data or 'url' not in data or 'prompt' not in data:
        return jsonify({'error': 'Missing "url" or "prompt" in request'}), 400
        
    page_url = data['url']
    user_prompt = data['prompt']
    
    try:
        # Get the response from the core processing function
        model_response = get_chat_response(user_prompt, page_url)
        # Return the response to the client
        return jsonify({'response': model_response})
    except Exception as e:
        # Return a generic error message if something goes wrong
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process the request.'}), 500

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)