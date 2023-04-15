from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class NoteBase(BaseModel):
    
    removed: str


class NoteGet(NoteBase):
    id: int
    cardTitle: str
    cardBody: str
    x: int
    y: int
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    is_active: bool
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class NoteCreate(NoteBase):
    cardTitle: str
    cardBody: str
    x: int
    y: int
    class Config:
        orm_mode = True

class NotePatch(NoteBase):
    cardTitle: str
    cardBody: str
    x: int
    y: int




