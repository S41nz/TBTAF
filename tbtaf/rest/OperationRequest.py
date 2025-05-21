from pydantic import BaseModel
from typing import Dict, Optional, List

class OperationRequest(BaseModel):
    suite_name: str
    tests_route: str = "./test/discoverer/samples"
    tags: Optional[List[str]] = None
    params: Optional[Dict] = None