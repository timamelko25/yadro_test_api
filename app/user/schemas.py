from pydantic import BaseModel


class StreetScheme(BaseModel):
    number: int
    name: str


class LocationScheme(BaseModel):
    street: StreetScheme
    city: str
    state: str
    country: str


class PictureScheme(BaseModel):
    thumbnail: str


class NameScheme(BaseModel):
    first: str
    last: str


class UserScheme(BaseModel):
    gender: str
    name: NameScheme
    phone: str
    email: str
    location: LocationScheme
    picture: PictureScheme
