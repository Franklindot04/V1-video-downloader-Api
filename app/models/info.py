from typing import Optional

from pydantic import BaseModel


class InfoResponse(BaseModel):
    title: Optional[str] = None
    uploader: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None