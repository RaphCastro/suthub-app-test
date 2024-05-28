from pydantic import BaseModel


class AgeGroup(BaseModel):
    min_age: int
    max_age: int
