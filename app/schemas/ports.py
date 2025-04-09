from pydantic import BaseModel
from typing import Optional

class PortSchema(BaseModel):
    numero: int
    status: Optional[str] = "open"

class PortResponse(PortSchema):
    id: int

    class Config:
        from_attributes = True
