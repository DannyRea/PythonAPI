from sql_app import schemas
import json

def format_recipe(recipe: schemas.RecipeCreate):
    recipe_dict = {}
    recipe_dict['id'] = recipe.id
    recipe_dict['idMeal'] = recipe.recipeId
    recipe_dict['strMeal'] = recipe.recipeName
    recipe_dict['strSource'] = recipe.recipeUrl
    recipe_dict['strMealThumb'] = recipe.recipeImgUrl
    
    for key, ingredient in json.loads(recipe.ingredients).items():
        recipe_dict[key] = ingredient
    for key, measurement in json.loads(recipe.measurements).items():
        recipe_dict[key] = measurement 
    recipe_dict['strInstructions'] = recipe.directions
    return recipe_dict
    