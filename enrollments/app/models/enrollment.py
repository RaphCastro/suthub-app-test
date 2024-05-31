from pydantic import BaseModel, Field


class Enrollment(BaseModel):
    name: str
    age: int
    cpf: str


class EnrollmentInDB(Enrollment):
    id: str = Field(default_factory=str)
