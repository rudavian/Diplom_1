from unittest.mock import Mock
import runpy
from pathlib import Path

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.database import Database
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    bun = Mock()
    bun.get_name.return_value = "black bun"
    bun.get_price.return_value = 100
    return bun


def make_ingredient(ingredient_type=INGREDIENT_TYPE_FILLING, name="cutlet", price=50):
    ingredient = Mock()
    ingredient.get_type.return_value = ingredient_type
    ingredient.get_name.return_value = name
    ingredient.get_price.return_value = price
    return ingredient


def test_set_buns_sets_bun(burger, bun):
    burger.set_buns(bun)

    assert burger.bun is bun


def test_add_ingredient_adds_ingredient(burger):
    ingredient = make_ingredient()

    burger.add_ingredient(ingredient)

    assert burger.ingredients == [ingredient]


def test_remove_ingredient_removes_ingredient_by_index(burger):
    first_ingredient = make_ingredient(name="cutlet")
    second_ingredient = make_ingredient(name="sauce")
    burger.add_ingredient(first_ingredient)
    burger.add_ingredient(second_ingredient)

    burger.remove_ingredient(0)

    assert burger.ingredients == [second_ingredient]


def test_move_ingredient_moves_ingredient_to_new_index(burger):
    first_ingredient = make_ingredient(name="cutlet")
    second_ingredient = make_ingredient(name="sauce")
    third_ingredient = make_ingredient(name="cheese")
    burger.add_ingredient(first_ingredient)
    burger.add_ingredient(second_ingredient)
    burger.add_ingredient(third_ingredient)

    burger.move_ingredient(0, 2)

    assert burger.ingredients == [second_ingredient, third_ingredient, first_ingredient]


@pytest.mark.parametrize(
    "bun_price, ingredient_prices, expected_price",
    [
        (100, [], 200),
        (100, [50], 250),
        (75.5, [10, 20.25], 181.25),
    ],
)
def test_get_price_returns_double_bun_price_plus_ingredients(
    burger, bun_price, ingredient_prices, expected_price
):
    bun = Mock()
    bun.get_price.return_value = bun_price
    burger.set_buns(bun)
    for price in ingredient_prices:
        burger.add_ingredient(make_ingredient(price=price))

    assert burger.get_price() == expected_price


def test_get_receipt_returns_burger_receipt(burger, bun):
    sauce = make_ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 30)
    filling = make_ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 50)
    burger.set_buns(bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)

    receipt = burger.get_receipt()

    assert receipt == (
        "(==== black bun ====)\n"
        "= sauce hot sauce =\n"
        "= filling cutlet =\n"
        "(==== black bun ====)\n\n"
        "Price: 280"
    )
    bun.get_name.assert_called()
    bun.get_price.assert_called()
    sauce.get_type.assert_called_once()
    filling.get_name.assert_called_once()


def test_burger_uses_real_database_items():
    database = Database()
    burger = Burger()
    bun = database.available_buns()[0]
    sauce = database.available_ingredients()[0]
    filling = database.available_ingredients()[3]

    burger.set_buns(bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)

    assert burger.get_price() == 400
    assert burger.get_receipt() == (
        "(==== black bun ====)\n"
        "= sauce hot sauce =\n"
        "= filling cutlet =\n"
        "(==== black bun ====)\n\n"
        "Price: 400"
    )


def test_bun_returns_name_and_price():
    bun = Bun("white bun", 200)

    assert bun.get_name() == "white bun"
    assert bun.get_price() == 200


def test_ingredient_returns_type_name_and_price():
    ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "sour cream", 200)

    assert ingredient.get_type() == INGREDIENT_TYPE_SAUCE
    assert ingredient.get_name() == "sour cream"
    assert ingredient.get_price() == 200


def test_praktikum_main_prints_burger_receipt(capsys):
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "praktikum.py"), run_name="__main__")

    receipt = capsys.readouterr().out

    assert "(==== black bun ====)" in receipt
    assert "= sauce sour cream =" in receipt
    assert "= filling dinosaur =" in receipt
    assert "Price: 700" in receipt
