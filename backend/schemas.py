from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "listener"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TrackCreate(BaseModel):
    title: str
    duration: str

class TrackResponse(TrackCreate):
    id: int
    author_id: int
    status: str
    class Config:
        from_attributes = True

class PlaylistCreate(BaseModel):
    title: str

class PlaylistAddTrack(BaseModel):
    track_id: int

class PlaylistResponse(BaseModel):
    id: int
    title: str
    user_id: int
    tracks: List[TrackResponse] = []
    class Config:
        from_attributes = True
