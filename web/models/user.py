import datetime
from uuid import uuid4, UUID

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel, create_engine, Session, Relationship, Enum
from typing import Optional
from enum import Enum as PyEnum
from sqlalchemy import DateTime, func

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

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )
    modified: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
class User(BaseModel,SQLModel, table=True):
    email: str = Field(sa_column=Column(String, unique=True))
    password: str
    username: str = Field(sa_column=Column(String, unique=True))

class Token(BaseModel, table=True):
    owner_id: UUID = Field(foreign_key="user.id")
    owner_type: str
    token_type: TokenType = Field(sa_column=Column(Enum(TokenType)), default=TokenType.OAUTH2)
    # Relationship to User
    # owner: Optional[User] = Relationship(back_populates="tokens")


class File(BaseModel, table=True):
    path: str
    size: int
    type: FileType = Field(sa_column=Column(Enum(FileType)))

class AnalysisRequest(BaseModel, table=True):
    content_id: str = Field()
    content_type: str
    status: AnalysisStatus = Field(sa_column=Column(Enum(AnalysisStatus)))

class AnalysisResult(BaseModel, table=True):
    analysis_request_id: UUID = Field(foreign_key="analysisrequest.id")
    processing_time: int
    status: ResultStatus = Field(sa_column=Column(Enum(ResultStatus)))
    # Relationship to AnalysisRequest
    # request: Optional[AnalysisRequest] = Relationship(back_populates="results")

