from decimal import Decimal
import random

from .constants import (
    first_names,
    last_names,
    recipe_titles,
    recipe_descriptions,
    recipe_times,
    recipe_prices,
    tags,
)

# Mock Data

# Helper Functions


def random_salt():
    """
    Helper function to generate a random salt with 3 digits.
    """
    return str(random.randrange(100, 1000))


def mock_user(**kwargs):
    """
    Helper function to create a mock user.
    """
    salt = kwargs.get("salt", random_salt())
    first_name = kwargs.get("first_name", random.choice(first_names))
    last_name = kwargs.get("last_name", random.choice(last_names))

    return {
        "first_name": first_name,
        "last_name": last_name,
        "username": f"{first_name.lower()}.{last_name.lower()}.{salt}",
        "email": f"{first_name.lower()}{last_name.lower()}{salt}@example.com",
        "password": f"pass_{reversed(first_name.lower())}{reversed(last_name.lower())}{salt}",
    }


def recipe_link(idx):
    """Helper function to create a link for a recipe."""
    title = recipe_titles[idx]
    return f"https://www.example.com/recipes/{title.lower().replace(' ', '-')}/"


def mock_recipe(**kwargs):
    """Helper function to create a mock recipe."""
    idx = kwargs.get("idx", random.randrange(len(recipe_titles)))
    title = kwargs.get("title", recipe_titles[idx])
    description = kwargs.get("description", recipe_descriptions[idx])
    time = kwargs.get("time", recipe_times[idx])
    price = kwargs.get("price", recipe_prices[idx])
    link = kwargs.get("link", recipe_link(idx))

    # user = kwargs.get("user", None)
    tags = kwargs.get("tags", [])

    recipe = {
        "title": title,
        "description": description,
        "time_minutes": time,
        "price": Decimal(str(price)),
        "link": link,
    }

    if tags:
        recipe["tags"] = tags

    # if user:
    #     recipe["user"] = user

    return recipe


def mock_tag(**kwargs):
    """Helper function to create a mock tag."""
    idx = kwargs.get("idx", random.randrange(len(tags)))
    name = kwargs.get("name", tags[idx])
    user = kwargs.get("user", None)

    tag = {"name": name}

    if user:
        tag["user"] = user

    return tag


# Mock Users

john_doe = mock_user(
    first_name="John",
    last_name="Doe",
)
