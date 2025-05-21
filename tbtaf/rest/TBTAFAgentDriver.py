from pydantic import BaseModel
from typing import Dict, Optional, List

class TBTAFAgentDriver(BaseModel):
    status: str  # "queued", "in_progress", "completed", "failed"
    progress: int
    results: Optional[List[Dict]] = None
    suite_name: str