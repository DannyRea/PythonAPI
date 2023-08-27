from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio
from sql_app import schemas, crud
from sql_app.models import Base
from sql_app.database import Base, SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from nasa.main import apod, mars_rover_photos
from meal.main import random_meal

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/notes", response_model=list[schemas.NoteGet])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_notes(db, skip=skip, limit=limit)


@app.get("/notes/{id}", response_model=schemas.NoteGet)
def read_note(id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db, id=id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_note


@app.post("/notes", response_model=schemas.NoteCreate)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    response = crud.create_note(db=db, note=note)
    return response


@app.patch("/notes/{id}", response_model=schemas.NotePatch)
def patch_note(id: str, note: schemas.NotePatch, db: Session = Depends(get_db)):
    print("here")
    stored_note_data = crud.get_note(db=db, id=id)

    update_data = note.dict()
    stored_note_data.id = update_data

    return update_data


@app.get("/apod")
def get_apod_image():
    return apod()


@app.get("/mars-rover-photos")
def get_mars_rover_photos():
    return mars_rover_photos()

@app.get("recipe")
async def get_all_recipes(db:Session = Depends(get_db)):
    pass

@app.get("/random-recipe")
def get_random_recipe(db:Session = Depends(get_db)):
    random_recipe = random_meal()
    print(random_recipe)
    db_recipe = crud.get_recipe(db=db, recipe=random_recipe)
   
    if not db_recipe:
        db_recipe = crud.create_recipe(db, random_recipe)
    return random_recipe


@app.post("/random-recipe", response_model=schemas.RecipeCreate)
async def create_recipe(recipe: schemas.RecipeCreate, db:Session = Depends(get_db)):
    db_recipe = await crud.create_recipe(db=db, recipe=recipe)
    return db_recipe
# @app.patch("/notes/{id}", response_model=schemas.NotePatch)
# def patch_note(id: int, note: schemas.NotePatch):
#     stored_data = note.dict()
#     stored_model = schemas.NotePatch(**stored_data)
#     update_data = note.dict(exclude_unset=True)
#     updated_data = stored_model.copy(update=update_data)
#     post = jsonable_encoder(updated_data)
#     return post
