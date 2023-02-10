from typing import TypedDict

Environment = TypedDict("Environment", {"REDIRECT_MAP_URL": str, "WEBROOT": str})


def get_redirect_map(env: Environment) -> str:
    return env["REDIRECT_MAP_URL"]


def calculate_env(redirect_map: str) -> Environment:
    return {"REDIRECT_MAP_URL": redirect_map, "WEBROOT": "/srv"}
