from pydantic import BaseModel
from typing import Dict, Optional


class SuitesResponse(BaseModel):
    project_name: str
    tags: Optional[Dict] = None