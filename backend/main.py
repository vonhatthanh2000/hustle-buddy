"""
FastAPI application for Hustle Buddy.
This file contains the API endpoints for the Hustle Buddy service.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from agent.agent import create_hustle_buddy_agent
from dotenv import load_dotenv
import uvicorn
import json
import os
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Hustle Buddy API", description="AI Model Response Evaluation API with Knowledge Base")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",  # React dev server
        "http://frontend:80",     # Docker frontend service
        "http://localhost:80",    # Direct nginx access
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to load knowledge base if available
knowledge_base = None
try:
    # Import knowledge base if available
    from agent.knowledge_rag import knowledge_base, load_knowledge_base
    print("Knowledge base module found.")
except ImportError:
    print("Knowledge base module not found. Running without knowledge base.")

# Create the agent with the knowledge base
hustle_buddy = create_hustle_buddy_agent(knowledge_base)

class ModelComparisonRequest(BaseModel):
    prompt: str
    model1: str
    model2: str
    model3: str
    use_knowledge: bool = False
    
    @validator('prompt', 'model1', 'model2', 'model3')
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid request format",
            "details": str(exc),
            "tip": "Make sure your JSON is properly formatted. Escape quotes with \\ and newlines with \\n"
        }
    )

@app.get("/")
async def root():
    return {
        "message": "Hustle Buddy API is running! Use POST /evaluate to analyze AI model responses.",
        "endpoints": {
            "evaluate": "POST /evaluate - Compare AI model responses",
            "knowledge-status": "GET /knowledge-status - Check knowledge base status",
            "load-knowledge": "POST /load-knowledge - Load/reload knowledge base",
            "docs": "GET /docs - Interactive API documentation",
            "health": "GET /health - Health check"
        },
        "features": {
            "knowledge_base": knowledge_base is not None,
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Hustle Buddy API"}

@app.get("/knowledge-status")
async def knowledge_status():
    """Check the status of the knowledge base."""
    if not knowledge_base:
        return {"status": "no_knowledge", "message": "No knowledge base available"}
    
    try:
        # Check if knowledge is loaded
        vector_db_exists = knowledge_base.vector_db.table_exists()
        return {
            "status": "ready" if vector_db_exists else "not_loaded",
            "knowledge_available": knowledge_base is not None,
            "vector_db_ready": vector_db_exists,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/load-knowledge")
async def load_knowledge(recreate: bool = False):
    """Load or reload the knowledge base from PDF files."""
    if not knowledge_base:
        raise HTTPException(status_code=400, detail="No knowledge base available")
    
    try:
        print(f"Loading knowledge base (recreate={recreate})...")
        load_knowledge_base(recreate=recreate)
        print("Knowledge base loaded successfully!")
        return {
            "status": "success",
            "message": "Knowledge base loaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading knowledge base: {str(e)}")

@app.post("/evaluate")
async def evaluate_models(request: ModelComparisonRequest):
    """
    Evaluate and compare responses from three AI models.
    
    Args:
        request: JSON with prompt, model_1, model_2, model_3 responses
        use_knowledge: Whether to use knowledge base for evaluation
        
    Returns:
        Analysis comparing Model 1 against Models 2 and 3
    """
    try:
        # Validate input lengths (optional safeguard)
        if len(request.prompt) > 10000:
            raise HTTPException(status_code=400, detail="Prompt too long (max 10,000 characters)")
        
        for field_name, field_value in [("model1", request.model1), ("model2", request.model2), ("model3", request.model3)]:
            if len(field_value) > 50000:
                raise HTTPException(status_code=400, detail=f"{field_name} response too long (max 50,000 characters)")
        
        # Construct the evaluation prompt
        evaluation_prompt = f"""
        Please analyze and compare the following AI model responses:

        **Original Prompt:**
        {request.prompt}

        **Model 1 Response:**
        {request.model1}

        **Model 2 Response:**
        {request.model2}

        **Model 3 Response:**
        {request.model3}

        Please evaluate Model 1 against Models 2 and 3 according to your instructions.
        """
        
        if request.use_knowledge and knowledge_base:
            evaluation_prompt += "\n\nPlease search your knowledge base for relevant evaluation criteria and best practices before providing your analysis."
        
        # Get the analysis from hustle_buddy
        response = hustle_buddy.run(evaluation_prompt)
        
        return {
            "status": "success",
            "analysis": response.content,
            "metadata": {
                "prompt_length": len(request.prompt),
                "model1_length": len(request.model1),
                "model2_length": len(request.model2),
                "model3_length": len(request.model3),
                "knowledge_used": request.use_knowledge and knowledge_base is not None,
                "session_id": response.session_id if hasattr(response, 'session_id') else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during evaluation: {str(e)}")

if __name__ == "__main__":
    # Load knowledge base on startup if available
    if knowledge_base:
        try:
            print("Loading knowledge base on startup...")
            load_knowledge_base(recreate=False)
            print("Knowledge base loaded successfully!")
        except Exception as e:
            print(f"Warning: Could not load knowledge base: {e}")
            print("You can load it manually using POST /load-knowledge")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)