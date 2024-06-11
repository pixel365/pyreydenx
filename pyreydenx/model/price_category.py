from pydantic import BaseModel


class PriceCategory(BaseModel):
    id: int
    is_active: bool
    name: str
    description: str
