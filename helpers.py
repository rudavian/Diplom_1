from unittest.mock import Mock

from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING


def make_ingredient(ingredient_type=INGREDIENT_TYPE_FILLING, name="cutlet", price=50):
    ingredient = Mock()
    ingredient.get_type.return_value = ingredient_type
    ingredient.get_name.return_value = name
    ingredient.get_price.return_value = price
    return ingredient
