from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class Node(BaseModel):
    id: str
    doc_id: str
    page: Optional[int] = None
    snippet: str
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None
