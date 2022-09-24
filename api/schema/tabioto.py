from typing import Optional, List

from pydantic import BaseModel, Field


class PlaceBase(BaseModel):
    name: Optional[str]
    latitude: float
    longitude: float


class Place(PlaceBase):
    id: int


class SoundBase(BaseModel):
    content: Optional[str]


class Sound(SoundBase):
    id: int


class SoundResponse(BaseModel):
    name: Optional[str]
    url: Optional[str]


class TabiotoDetailResponse(BaseModel):
    place: Place
    sound_list: List[SoundResponse]
    place_count: int


class TabiotoCreateRequest(BaseModel):
    user_id: int
    title: Optional[str]
    content: Optional[str]


class TabiotoCreateResponse(BaseModel):
    title: Optional[str]
    sound_url: Optional[str]
