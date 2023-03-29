# Copyright 2022 Canonical
# See LICENSE file for licensing details.

from unittest.mock import MagicMock, patch

import pytest
from charms.nginx_ingress_integrator.v0.ingress import IngressRequires

from ingress import init, update

@pytest.fixture(name="ingress_config")
def ingress_config_fixture():
    return {"external-hostname": "site.url"}

@pytest.fixture(name="expected_ingress_config")
def expected_ingress_config_fixture():
    return {"service-hostname": "site.url"}

@patch("charms.nginx_ingress_integrator.v0.ingress.IngressRequires.__new__")
def test_init(mock, ingress_config, expected_ingress_config) -> None:
    """
    arrange: A mocked charm and an ingress configuration that has an external-hostname
    act: The init method is called
    expect: An IngressRequires is instanciated using an ingress configuration that has a
    service-hostname and no external-hostname
    """
    charm = MagicMock()
    init(charm, ingress_config)

    mock.assert_called_once_with(IngressRequires, charm, expected_ingress_config)

@patch("charms.nginx_ingress_integrator.v0.ingress.IngressRequires.__new__")
def test_init_no_service_hostname(mock) -> None:
    """
    arrange: A mocked charm and an ingress configuration that has an external-hostname
    act: The init method is called
    expect: An IngressRequires is instanciated using an ingress configuration that has a
    service-hostname and no external-hostname
    """
    charm = MagicMock()
    init(charm, {})

    mock.assert_called_once_with(IngressRequires, charm, {})

def test_update(ingress_config, expected_ingress_config) -> None:
    """
    arrange: A mocked IngressRequires instance and an ingress configuration that has an external-hostname
    act: The update method is called
    expect: The update_config method of IngressRequires is called using an ingress configuration that has
    a service-hostname and no external-hostname
    """
    mock = MagicMock()

    update(mock, ingress_config)

    mock.update_config.assert_called_once_with(expected_ingress_config)

def test_update_no_service_hostname() -> None:
    """
    arrange: A mocked IngressRequires instance and an ingress configuration without external-hostname
    act: The update method is called
    expect: The update_config method of IngressRequires is called using an ingress configuration without
    external-hostname
    """
    mock = MagicMock()
    ingress_config = {}

    update(mock, ingress_config)

    mock.update_config.assert_called_once_with(ingress_config)