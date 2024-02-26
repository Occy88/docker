from datetime import datetime
from enum import Enum as PyEnum
from uuid import uuid4, UUID

import pytz
from sqlalchemy import Column, String, DateTime
from sqlmodel import Field, SQLModel, Enum


class TokenType(PyEnum):
    OAUTH2 = "oauth2"

class FileType(PyEnum):
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"

class AnalysisStatus(PyEnum):
    OPEN = "open"
    PROCESSING = "processing"
    COMPLETE = "complete"

class ResultStatus(PyEnum):
    SUCCESS = "success"
    ERROR = "error"
def get_field():
    return Field(sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(
        pytz.timezone('Europe/London'))))

class BaseSQLModel(SQLModel):
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = False
    id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at:datetime
    updated_at:datetime
    date_chosen:datetime
    def __init_subclass__(cls, **kwargs):
        cls.__tablename__=str(cls.__name__).lower()
        cls.created_at: datetime = get_field()
        cls.updated_at: datetime = get_field()
        cls.date_chosen: datetime = get_field()
        super().__init_subclass__(**kwargs)


class BaseMixin:
    ...
class User(BaseMixin,BaseSQLModel, table=True):
    email: str = Field(sa_column=Column(String, unique=True))
    password: str
    username: str = Field(sa_column=Column(String, unique=True))

class Token(BaseMixin,BaseSQLModel, table=True):
    owner_id: UUID = Field(foreign_key="user.id")
    owner_type: str
    token_type: TokenType = Field(sa_column=Column(Enum(TokenType)), default=TokenType.OAUTH2)
    # Relationship to User
    # owner: Optional[User] = Relationship(back_populates="tokens")


class File(BaseMixin,BaseSQLModel, table=True):
    path: str
    size: int
    type: FileType = Field(sa_column=Column(Enum(FileType)))

class AnalysisRequest(BaseMixin,BaseSQLModel, table=True):
    content_id: str = Field()
    content_type: str
    status: AnalysisStatus = Field(sa_column=Column(Enum(AnalysisStatus)))

class AnalysisResult(BaseMixin,BaseSQLModel, table=True):
    analysis_request_id: UUID = Field(foreign_key="analysisrequest.id")
    processing_time: int
    status: ResultStatus = Field(sa_column=Column(Enum(ResultStatus)))
    # Relationship to AnalysisRequest
    # request: Optional[AnalysisRequest] = Relationship(back_populates="results")

