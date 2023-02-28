#!/usr/bin/env python3
# Copyright 2021 Jon Seager
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus, WaitingStatus

logger = logging.getLogger(__name__)


from ops.charm import CharmBase

from gosherve import calculate_env as calculate_gosherve_env
from ingress import set_ as set_ingress
from site_ import set_local_content as set_site_content
from state import State

APPLICATION_NAME = "gosherve"


class HelloKubeconCharm(CharmBase):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.framework.observe(self.on.install, self._update_site_content)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.gosherve_pebble_ready, self._update_containers)

        self.framework.observe(self.on.pull_site_action, self._pull_site_action)

        self.state = State(self)

    def _on_config_changed(self, event=None) -> None:
        self._update_ingress(event)
        self._update_containers(event)

    def _update_containers(self, _event=None) -> None:
        self.unit.status = MaintenanceStatus("Getting application ready")

        container = self.unit.get_container(APPLICATION_NAME)

        if not container.can_connect():
            self.unit.status = WaitingStatus("waiting for Pebble in workload container")
            return

        gosherve_env = calculate_gosherve_env(self.state.redirect_map)
        gosherve_layer = {
            "summary": f"{APPLICATION_NAME} layer",
            "description": f"pebble config layer for {APPLICATION_NAME}",
            "services": {
                APPLICATION_NAME: {
                    "override": "replace",
                    "summary": APPLICATION_NAME,
                    "command": "/gosherve",
                    "startup": "enabled",
                    "environment": gosherve_env,
                }
            },
        }
        container.add_layer(APPLICATION_NAME, gosherve_layer, combine=True)
        container.pebble.replan_services()

        self.unit.status = ActiveStatus()

    def _update_ingress(self, _event=None) -> None:
        self.ingress = set_ingress(
            self, getattr(self, "ingress", None), self.state.ingress
        )

    def _update_site_content(self, _event=None) -> None:
        set_site_content(self.state.site_content)

    def _pull_site_action(self, event) -> None:
        self._update_site_content()
        event.set_results({"result": "site pulled"})


if __name__ == "__main__":
    main(HelloKubeconCharm)
