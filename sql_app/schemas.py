from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class NoteBase(BaseModel):
    removed: str


class RecipeBase(BaseModel):
    recipeId: int


class CalenderEventBase(BaseModel):
    id: int
    removed: str


class NoteGet(NoteBase):
    id: int
    noteTitle: str
    noteBody: str

    class Config:
        orm_mode = True


class RecipeGet(RecipeBase):
    recipeUrl: str
    recipeName: str
    recipeImgUrl: str
    recipyVideoUrl: str
    ingredients: str
    measurements: str
    directions: str


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


class RecipeCreate(RecipeBase):
    recipeUrl: str
    recipeName: str
    recipeImgUrl: str
    recipyVideoUrl: str
    ingredients: str
    measurements: str
    directions: str


class CalenderEventGet(CalenderEventBase):
    eventTitle: str
    eventTimeStart: str
    eventTimeEnd: str
    eventDateStart: str
    eventDateEnd: str
    eventBody: str


class CalenderEventCreate(CalenderEventBase):
    eventTitle: str
    eventTimeStart: str
    eventTimeEnd: str
    eventDateStart: str
    eventDateEnd: str
    eventBody: str
    createdTime: str
    createdDate: str
