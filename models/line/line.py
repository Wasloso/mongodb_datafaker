from typing import List
from pydantic import Field
from models.line.pathItem import PathItem
from models.model import Model


class Line(Model):
    number: str = Field(min_length=1)
    path: List[PathItem] = Field(min_items=2)
