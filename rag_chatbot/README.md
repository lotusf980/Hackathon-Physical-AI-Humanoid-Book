# RAG Chatbot Backend

A Retrieval-Augmented Generation (RAG) chatbot backend built with FastAPI.

## Features

- FastAPI-based REST API
- RAG (Retrieval-Augmented Generation) architecture
- Integration with OpenAI for chat completions
- Vector search with Qdrant (placeholder implementation)
- Clean, modular code structure

## Architecture

```
rag_chatbot/
├── main.py                 # FastAPI application entry point
├── start_server.py         # Server startup script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── api/
│   └── routers/
│       └── chat.py        # Chat API endpoints
├── models/
│   └── chat.py            # Pydantic models
├── services/
│   ├── chat_service.py    # Main chat service orchestrator
│   ├── openai_service.py  # OpenAI integration
│   └── vector_search.py   # Vector search (Qdrant) service
├── utils/
│   └── embedding.py       # Embedding utilities
└── config/
    └── settings.py        # Configuration and settings
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_openai_api_key
export QDRANT_HOST=localhost
export QDRANT_PORT=6333
export QDRANT_COLLECTION=documents
```

3. Start the server:
```bash
python start_server.py
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/chat` - Chat endpoint

### Chat Endpoint

**URL**: `POST /api/v1/chat`

**Request Body**:
```json
{
  "question": "Your question here",
  "selected_text": "Optional selected text for context",
  "context": ["Optional", "Context", "Strings"],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "response": "Generated response",
  "sources": ["source1", "source2"],
  "tokens_used": 150,
  "context_used": ["context1", "context2"]
}
```

## Configuration

The application uses the following environment variables:

- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - OpenAI model to use (default: gpt-3.5-turbo)
- `QDRANT_HOST` - Qdrant host (default: localhost)
- `QDRANT_PORT` - Qdrant port (default: 6333)
- `QDRANT_COLLECTION` - Qdrant collection name (default: documents)
- `DEBUG` - Enable debug mode (default: False)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)