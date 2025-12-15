# Website Assistant - Chrome Extension

An intelligent Chrome extension that allows you to chat with any webpage using AI. Ask questions about the content, get summaries, extract information, and more—all without leaving your browser.

## Features

✨ **AI-Powered Q&A** - Ask questions about any webpage and get intelligent answers  
📄 **Content Awareness** - The AI reads and understands the full page content  
🚀 **Fast & Efficient** - RAG (Retrieval-Augmented Generation) for accurate, contextual responses  
💬 **Clean UI** - Modern, glassmorphic interface integrated directly into your browser  
🔒 **Private** - Process pages locally through your own backend server  

## How It Works

1. **Open any webpage** in Chrome
2. **Click the Website Assistant extension icon** to open the popup
3. **Ask a question** about the page content
4. **Get an AI-generated response** within seconds

The extension leverages **LangChain** with **HuggingFace LLMs** to:
- Load and parse webpage content
- Split content into semantic chunks
- Create embeddings for retrieval
- Perform retrieval-augmented generation (RAG)
- Return concise, contextual answers

## Prerequisites

- **Python 3.8+**
- **Chrome/Chromium browser**
- **HuggingFace API token** (for LLM access)

## Installation & Setup

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- `flask`
- `flask-cors`
- `langchain-huggingface`
- `langchain`
- `langchain-community`
- `chromadb`
- `python-dotenv`

### 2. Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
```

Get your token from: https://huggingface.co/settings/tokens

### 3. Start the Backend Server

```bash
cd backend
python app.py
```

The server will run on `http://127.0.0.1:5000`

### 4. Install the Chrome Extension

1. Open `chrome://extensions/` in your browser
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Navigate to the `extension/` folder and select it
5. The extension should now appear in your extensions list

## Usage

1. **Navigate to any website** you want to ask about
2. **Click the Website Assistant icon** in your extension bar
3. **Enter your question** in the text area (e.g., "Summarize this article", "What are the main points?")
4. **Click "Ask AI"** and wait for the response
5. **Read the answer** in the response area

## Project Structure

```
Website Assistant/
├── backend/
│   ├── app.py          # Flask server with LangChain RAG pipeline
│   ├── test.py         # Testing utilities
│   └── requirements.txt # Python dependencies
├── extension/
│   ├── index.html      # Popup UI with styling
│   ├── popup.js        # Extension logic and communication
│   ├── manifest.json   # Chrome extension manifest
└── README.md           # This file
```

## Architecture

### Frontend (Chrome Extension)
- `index.html` - Modern popup UI with glassmorphic design
- `popup.js` - Handles tab URL detection and backend communication

### Backend (Python Flask)
- `app.py` - REST API endpoint for chat requests
  - Uses HuggingFace Endpoints for LLM inference
  - Implements LangChain's RAG pipeline
  - Vector storage with Chroma DB
  - Semantic search for context retrieval

## API Endpoint

### POST `/chat`

**Request:**
```json
{
  "url": "https://example.com/article",
  "prompt": "What is this article about?"
}
```

**Response:**
```json
{
  "response": "This article discusses..."
}
```

**Error Response:**
```json
{
  "error": "Missing 'url' or 'prompt' in request"
}
```

## Configuration

### Backend Settings

Edit `backend/app.py` to customize:

- **Text Chunking**: Modify `RecursiveCharacterTextSplitter` parameters
  - `chunk_size`: Size of text chunks (default: 1000)
  - `chunk_overlap`: Overlap between chunks (default: 200)

- **Embedding Model**: Currently uses `sentence-transformers/all-MiniLM-L6-v2`
  - Can be swapped for other HuggingFace embedding models

- **LLM Model**: Currently uses `openai/gpt-oss-120b`
  - Configure different models as needed

### Extension Permissions

The extension requires:
- `activeTab` - Access to the current tab's URL
- `host_permissions` for `http://127.0.0.1:5000/*` - Local backend communication

## Troubleshooting

### "Could not connect to the backend"
- Ensure the Flask server is running: `python backend/app.py`
- Check that the server is accessible at `http://127.0.0.1:5000`
- Verify CORS is enabled in Flask

### "Cannot get URL. Try a valid website"
- Only HTTP/HTTPS websites are supported
- Some restricted pages (chrome://, file://) cannot be accessed

### No response from AI
- Check your HuggingFace API token is valid
- Ensure you have sufficient API quota
- Check backend console for error messages

## Development

### Running Tests

```bash
cd backend
python test.py
```

### Debugging the Extension

1. Open `chrome://extensions/`
2. Find "Website Assistant" and click **Details**
3. Click **Inspect views: background page** for debugging


## License

MIT License - Feel free to use and modify this project.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**Built with:** LangChain • HuggingFace • Flask • Chrome Extension API