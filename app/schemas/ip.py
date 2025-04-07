from pydantic import BaseModel
from typing import Optional


class IPSchema(BaseModel):
    adresse_ip: str
    port: int
class IPResponse(IPSchema):
    id: Optional[int]
    status: str
    affect_id: int

    class Config:
        from_attributes = True
