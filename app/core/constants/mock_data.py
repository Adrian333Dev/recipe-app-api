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


# Mock Users

john_doe = mock_user(
    "John",
    "Doe",
)
