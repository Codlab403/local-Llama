from pydantic import BaseModel
from typing import List, Optional


class Document(BaseModel):
    id: str
    filename: str
    uploaded_at: Optional[str] = None
    status: Optional[str] = None
    pages: Optional[int] = None
    size_kb: Optional[float] = None
    tags: Optional[List[str]] = None
