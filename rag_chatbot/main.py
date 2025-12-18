from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import chat

app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot backend",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development - tighten security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers so frontend can read response headers if needed
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add OPTIONS endpoint for CORS preflight requests
@app.options("/api/v1/chat")
async def chat_options():
    return {"status": "ok"}

# Add a test endpoint to verify connectivity
@app.get("/api/v1/test")
async def test_connection():
    return {"status": "connected", "message": "Successfully connected to RAG Chatbot API"}