from pydantic import BaseModel, Field
from typing import List, Optional

class Source(BaseModel):
    title: str = Field(description="The title of the documentation page")
    url: str = Field(description="The direct link to the documentation")

class ChatResponse(BaseModel):
    answer: str = Field(description="The detailed markdown response from the AI")
    sources: List[Source] = Field(default_factory=list, description="List of reference links")