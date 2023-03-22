# Copyright 2022 Canonical
# See LICENSE file for licensing details.

from unittest.mock import MagicMock, patch

import pytest
from ops.testing import Harness

from charm import HelloKubeconCharm
from state import State


@pytest.fixture(name="harness")
def harness_fixture():
    """Ops testing framework harness fixture."""
    harness = Harness(HelloKubeconCharm)

    yield harness

    harness.cleanup()


def test_init(harness: Harness):
    patch_ingress = patch("charm.init_ingress")
    patch_state = patch("state.State.__new__", autospec=True)

    mock_ingress = patch_ingress.start()
    mock_state = patch_state.start()

    harness.begin()

    mock_ingress.assert_called_once()
    mock_state.assert_called_once_with(
        State, harness.charm.config, harness.charm.app.name
    )

    patch.stopall()
