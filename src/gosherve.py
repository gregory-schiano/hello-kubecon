from typing import TypedDict

Environment = TypedDict("Environment", {"REDIRECT_MAP_URL": str, "WEBROOT": str})


def calculate_env(redirect_map: str) -> Environment:
    return {"REDIRECT_MAP_URL": redirect_map, "WEBROOT": "/srv"}
