from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    telegram_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    profile: Optional[str] = None
    reading: Optional[str] = None

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None
        }

class User(UserCreate):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str
    updated_at: str

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None
        }

    def to_dynamodb_item(self) -> dict:
        item = self.model_dump(exclude_none=True)
        if 'date_of_birth' in item and item['date_of_birth']:
            item['date_of_birth'] = item['date_of_birth'].isoformat()
        return item

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> 'User':
        if 'date_of_birth' in item and item['date_of_birth']:
            item['date_of_birth'] = date.fromisoformat(item['date_of_birth'])
        return cls(**item)
