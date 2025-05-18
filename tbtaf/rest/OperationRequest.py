from pydantic import BaseModel
from typing import Dict, Optional, List

class OperationRequest(BaseModel):
    suite_name: str
    tags: Optional[List[str]] = None
    params: Optional[Dict] = None