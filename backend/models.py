from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class STLCInput(BaseModel):
    requirements: str = Field(..., description="Software requirements or user stories.")
    user_stories: Optional[str] = Field(None, description="Detailed user stories.")
    code_diffs: Optional[str] = Field(None, description="Code changes in diff format (e.g., from Git).")
    previous_test_results: Optional[str] = Field(None, description="Previous test execution logs or summaries.")

class STLCResponse(BaseModel):
    run_id: str = Field(..., description="Unique ID for the STLC run.")
    status: str = Field(..., description="Current status of the STLC process.")
    output: Dict[str, Any] = Field({}, description="Outputs from various agents or current state.")
    messages: List[str] = Field([], description="Log messages or status updates.")
    error: Optional[str] = Field(None, description="Any error message, if applicable.")