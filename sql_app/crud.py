from sqlalchemy.orm import Session

from . import models, schemas
from utils.recipe import format_recipe
from utils.dateutils import database_date
from utils.timeutils import database_time
import json


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_note(db: Session, id: int):
    return db.query(models.Note).filter(models.Note.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def get_all_recipes(db: Session):
    all_recipes = db.query(models.Recipe).all()

    formatted_recipes = [format_recipe(recipe) for recipe in all_recipes]
    return formatted_recipes or []


def get_recipe(db: Session, recipe: schemas.RecipeGet):
    return (
        db.query(models.Recipe)
        .filter(models.Recipe.recipeId == int(recipe["meals"][0]["idMeal"]))
        .first()
    )


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(
        cardTitle=note.cardTitle, cardBody=note.cardBody, x=note.x, y=note.y
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    meal = recipe["meals"][0]

    ingredients_dict_str = json.dumps(
        {key: value for (key, value) in meal.items() if "Ingredient" in key}
    )
    measurements_dict_str = json.dumps(
        {key: value for (key, value) in meal.items() if "Measure" in key}
    )

    db_recipe = models.Recipe(
        recipeId=int(meal["idMeal"]),
        recipeName=meal["strMeal"],
        recipeUrl=meal["strSource"],
        recipeImgUrl=meal["strMealThumb"],
        ingredients=ingredients_dict_str,
        measurements=measurements_dict_str,
        directions=meal["strInstructions"],
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def create_event(db: Session, event: schemas.CalenderEventCreate):
    db_event = models.CalenderEvent(
        eventTitle=event["eventTitle"],
        eventTimeStart=event["eventTimeStart"],
        eventTimeEnd=event["eventTimeEnd"],
        eventDateStart=event["eventDateStart"],
        eventDateEnd=event["eventDateEnd"],
        eventBody=event["eventBody"],
        createdTime=database_time(),
        createdDate=database_date(),
    )
    print("db_event", db_event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CalenderEvent).offset(skip).limit(limit).all()


def delete_recipe(db: Session, id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
    return db_recipe
