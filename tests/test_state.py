# Copyright 2022 Canonical
# See LICENSE file for licensing details.

import pytest

from state import State


@pytest.fixture(name="charm_name")
def charm_name_fixture():
    yield "test"


@pytest.fixture(name="charm_config")
def charm_config_fixture():
    yield {"external-hostname": "site.url", "redirect-map": "https://site.url/path"}


def test_ingress(charm_name: str, charm_config: dict[str, str]) -> None:
    """
    arrange: A charm config containing an external-hostname and a charm name
    act: Create a state
    assert: The state ingress property contains the expected values
    """
    state = State(charm_config, charm_name)

    expected = {
        "external-hostname": charm_config["external-hostname"],
        "service-name": charm_name,
        "service-port": 8080,
    }

    assert state.ingress == expected


def test_ingress_no_external_hostname(charm_name: str) -> None:
    """
    arrange: A charm config containing an empty external-hostname and a charm name
    act: Create a state
    assert: The state ingress property contains the expected values
    """
    config = {"external-hostname": None}
    state = State(config, charm_name)

    expected = {
        "external-hostname": charm_name,
        "service-name": charm_name,
        "service-port": 8080,
    }

    assert state.ingress == expected

def test_redirect_map_url(charm_name: str, charm_config: dict[str, str]) -> None:
    """
    arrange: A charm config containing an URL in the redirect-map and a charm name
    act: Create a state
    assert: The state redirect_map_url property contains the expected values
    """
    state = State(charm_config, charm_name)

    expected = charm_config["redirect-map"]
    
    assert state.redirect_map_url == expected