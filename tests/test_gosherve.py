# Copyright 2022 Canonical
# See LICENSE file for licensing details.

import pytest

from gosherve import calculate_env

def test_calculate_env() -> None:
    """
    arrange: a redirect_map url is set
    act: the environment is generated
    assert: the environemnt contains the redirect_map_url and a webroot variables
    """
    redirect_map_url = "https://test.url/path"
    environment = calculate_env(redirect_map_url)

    expected = {"REDIRECT_MAP_URL": redirect_map_url, "WEBROOT": "/srv"}
    assert environment ==  expected