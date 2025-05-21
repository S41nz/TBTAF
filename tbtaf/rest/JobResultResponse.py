from pydantic import BaseModel
from typing import Dict, Optional, List

class JobResultResponse(BaseModel):
    job_id: str
    results: Optional[List[Dict]] = None
    summary: str