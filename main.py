from fastapi import FastAPI, Depends, HTTPException
import socketio
from fastapi_socketio import SocketManager
from sqlalchemy.orm import Session
from sql_app import schemas, crud
from sql_app.models import Base
from sql_app.database import Base, SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from nasa.main import apod, mars_rover_photos
from meal.main import random_meal

app = FastAPI()
origins = "*"
sio = socketio.AsyncServer(cors_allowed_origins=origins, async_mode="asgi")

socket_app = socketio.ASGIApp(sio)

background_task_started = False


app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


connections = []


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit("my_response", {"data": "Server generated event"})


@sio.on("connect")
def connect(sid, data):
    connections.append(sid)


@sio.on("disconnect")
def disconnect(sid, data):
    connections.pop(connections.index(sid))


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


@app.route("/users")
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.route("/users")
@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.route("/users/{user_id}")
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.route("/notes")
@app.get("/notes", response_model=list[schemas.NoteGet])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_notes(db, skip=skip, limit=limit)


@app.route("/notes/{id}")
@app.get("/notes/{id}", response_model=schemas.NoteGet)
def read_note(id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db, id=id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_note


@app.route("/notes")
@app.post("/notes", response_model=schemas.NoteCreate)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    response = crud.create_note(db=db, note=note)
    return response


@app.route("/notes/{id}")
@app.patch("/notes/{id}", response_model=schemas.NotePatch)
def patch_note(id: str, note: schemas.NotePatch, db: Session = Depends(get_db)):
    stored_note_data = crud.get_note(db=db, id=id)

    update_data = note.dict()
    stored_note_data.id = update_data

    return update_data


@app.route("/apod")
@app.get("/apod")
def get_apod_image():
    return apod()


@app.route("/mars-rover-photos")
@app.get("/mars-rover-photos")
def get_mars_rover_photos():
    return mars_rover_photos()


@app.route("/recipes")
@app.get("/recipes")
async def get_all_recipes(db: Session = Depends(get_db)):
    return crud.get_all_recipes(db=db)


@app.route("/random-recipe")
@app.get("/random-recipe")
async def get_random_recipe(db: Session = Depends(get_db)):
    random_recipe = random_meal()
    db_recipe = crud.get_recipe(db=db, recipe=random_recipe)

    if not db_recipe:
        db_recipe = crud.create_recipe(db, random_recipe)
        print("hjere")
        await sio.emit("recipes", {"data": await get_all_recipes(db=db)})
    return random_recipe


@app.route("/random-recipe")
@app.post("/random-recipe", response_model=schemas.RecipeCreate)
async def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = await crud.create_recipe(db=db, recipe=recipe)
    return db_recipe


@app.route("/recipes/{id}")
@app.delete("/recipes/{id}")
async def delete_recipe(id, db: Session = Depends(get_db)):
    result = crud.delete_recipe(db=db, id=id)
    await sio.emit("recipes", {"data": await get_all_recipes(db=db)})
    return result


app.mount("/", socket_app)
# @app.patch("/notes/{id}", response_model=schemas.NotePatch)
# def patch_note(id: int, note: schemas.NotePatch):
#     stored_data = note.dict()
#     stored_model = schemas.NotePatch(**stored_data)
#     update_data = note.dict(exclude_unset=True)
#     updated_data = stored_model.copy(update=update_data)
#     post = jsonable_encoder(updated_data)
#     return post
