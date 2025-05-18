from pydantic import BaseModel
from typing import Dict, Optional, List

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    results: Optional[List[Dict]] = None