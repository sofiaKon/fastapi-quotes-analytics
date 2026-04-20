from pydantic import BaseModel


class QuoteCreate(BaseModel):
    text: str
    author: str
    category: str


class QuoteUpdate(BaseModel):
    text: str
    author: str
    category: str


class QuoteResponse(BaseModel):
    id: int
    text: str
    author: str
    category: str

    class Config:
        from_attributes = True
