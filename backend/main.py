import os
import vertexai

from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the Orchestrator
from backend.orchestrator.stlc_orchestrator import Orchestrator, STLCGraphState
from backend.models import STLCInput 

load_dotenv()

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION")

if not PROJECT_ID or not REGION:
    # Changed from exit(1) to raising an exception, which FastAPI will catch and handle appropriately
    # (e.g., return a 500 error if it happens during handler execution, or prevent startup)
    raise RuntimeError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION must be set. Ensure they are configured as environment variables in Cloud Run.")

# Vertex AI initialization. Rely on Cloud Run's assigned service account for authentication.
# No need for GOOGLE_APPLICATION_CREDENTIALS env var if service account is properly configured.
try:
    vertexai.init(project=PROJECT_ID, location=REGION)
    print(f"Vertex AI initialized for project: {PROJECT_ID}, region: {REGION}")
except Exception as e:
    # Log the error but don't exit the process immediately.
    # If this fails, subsequent calls to Vertex AI will likely fail and raise errors.
    print(f"Warning: Error initializing Vertex AI: {e}")
    print("Ensure your Cloud Run service account has the necessary permissions (e.g., Vertex AI User).")


app = FastAPI(
    title="Risk & Compliance AI Agent System",
    description="Backend for STLC AI Agents with intelligent routing.",
    version="0.1.0",
)

# CORS middleware to allow frontend to communicate with backend
# Adjust origins based on your frontend's deployment URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Orchestrator instance, passing the LLM
orchestrator_instance = Orchestrator()


# class ChatRequest(BaseModel):
#     requirements: str
#     user_stories: Optional[str] = "default_user"
#     session_id: Optional[str] = "default_session"
#     tenant_id: Optional[str] = "default_tenant"
#     api_key: str # This would be the Lab45 API key if you need to use their tools
#     dataset_id: Optional[str] = None # For RAG relevant agents

@app.post("/chat")
async def chat_endpoint(request: STLCInput):
    try:
        # STLCGraphState state
        # Pass all relevant parameters to the workflow
        # not necessarily the Vertex AI authentication (which relies on GCP ADC).
        response_content = orchestrator_instance.run_stlc(request.model_dump()
                                                                
        )
        print("\n--- Final results ---\n")
        print(response_content)
        return {"response": response_content}
    except Exception as e:
        print(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "STLC AI Agent System Backend is running!"}