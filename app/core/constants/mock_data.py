from decimal import Decimal
from .constants import recipe_titles, recipe_descriptions, recipe_times, recipe_prices

# Mock Data

# Helper Functions


def mock_user(first_name, last_name, salt="666"):
    """
    Helper function to create a mock user.
    """
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
    idx = kwargs.get("idx", 0)
    title = kwargs.get("title", recipe_titles[idx])
    description = kwargs.get("description", recipe_descriptions[idx])
    time = kwargs.get("time", recipe_times[idx])
    price = kwargs.get("price", recipe_prices[idx])
    link = kwargs.get("link", recipe_link(idx))
    user = kwargs.get("user", None)

    recipe = {
        "title": title,
        "description": description,
        "time_minutes": time,
        "price": price,
        "link": link,
    }
    if user:
        recipe["user"] = user

    return recipe


# Mock Users

john_doe = mock_user(
    "John",
    "Doe",
)
