# Copyright 2022 Canonical
# See LICENSE file for licensing details.

from unittest.mock import MagicMock, patch

import pytest
from ops.model import ActiveStatus, MaintenanceStatus, WaitingStatus
from ops.testing import Harness

from charm import APPLICATION_NAME, HelloKubeconCharm
from state import State


@pytest.fixture(name="harness")
def harness_fixture():
    """Ops testing framework harness fixture."""
    harness = Harness(HelloKubeconCharm)

    yield harness

    harness.cleanup()


def test_init(monkeypatch, harness: Harness):
    mock_ingress = MagicMock()
    monkeypatch.setattr("charm.init_ingress", mock_ingress)

    harness.begin()
    mock_ingress.assert_called_once()

    assert isinstance(harness.charm.state, State)
    assert harness.charm.state._charm_config == harness.charm.config
    assert harness.charm.state._charm_name == harness.charm.app.name

def test_update_containers_cannot_connect(harness: Harness) -> None:
    harness.begin()
    harness.charm._update_containers()

    assert isinstance(harness.charm.unit.status, WaitingStatus)
    assert harness.charm.unit.status.message == "waiting for Pebble in workload container"

def test_update_containers(monkeypatch, harness: Harness) -> None:
    harness.set_can_connect(harness.model.unit.containers[APPLICATION_NAME], True)
    harness.begin()
    env = {"SOME_ENV": "some_value"}
    mock_calculate_gosherve_env = MagicMock()
    mock_calculate_gosherve_env.return_value = env
    monkeypatch.setattr("charm.calculate_gosherve_env", mock_calculate_gosherve_env)

    harness.charm._update_containers()

    mock_calculate_gosherve_env.assert_called_once()
    assert isinstance(harness.charm.unit.status, ActiveStatus)
    assert harness.model.unit.get_container(APPLICATION_NAME).get_plan().to_dict() == {
            "services": {
                APPLICATION_NAME: {
                    "override": "replace",
                    "summary": APPLICATION_NAME,
                    "command": "/gosherve",
                    "startup": "enabled",
                    "environment": env,
                }
            },
        }

def test_pebble_ready(monkeypatch, harness: Harness) -> None:
    mock_update_containers = MagicMock()

    harness.set_can_connect(harness.model.unit.containers[APPLICATION_NAME], True)
    harness.begin()

    monkeypatch.setattr(harness.charm, "_update_containers", mock_update_containers)

    harness.container_pebble_ready(APPLICATION_NAME)

    mock_update_containers.assert_called_once()

def test_pull_site_action(monkeypatch, harness: Harness) -> None:
    event_mock = MagicMock()
    event_mock.set_results = MagicMock()
    
    mock_set_site_content = MagicMock()
    monkeypatch.setattr("charm.set_site_content", mock_set_site_content)

    harness.set_can_connect(harness.model.unit.containers[APPLICATION_NAME], True)
    harness.begin()
     
    harness.charm._pull_site_action(event_mock)

    mock_set_site_content.assert_called_once()
    event_mock.set_results.assert_called_once_with({"result": "site pulled"})
