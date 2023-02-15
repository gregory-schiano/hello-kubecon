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
from state import Actual, Desired


class HelloKubeconCharm(CharmBase):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.framework.observe(self.on.install, self._reconcile_site_content)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(
            self.on.gosherve_pebble_ready, self._reconcile_redirect_map
        )

        self.framework.observe(self.on.pull_site_action, self._pull_site_action)

        self.ingress = None
        self.actual = Actual(self)
        self.desired = Desired(self)

        self._reconcile_ingress()

    def _on_config_changed(self, event=None) -> None:
        self._reconcile_ingress(event)
        self._reconcile_redirect_map(event)

    def _reconcile_redirect_map(self, _event=None) -> None:
        if self.desired.redirect_map == self.actual.redirect_map:
            return

        self.unit.status = MaintenanceStatus("Setting redirect map")
        gosherve_env = calculate_gosherve_env(self.desired.redirect_map)
        gosherve_layer = {
            "summary": "gosherve layer",
            "description": "pebble config layer for gosherve",
            "services": {
                "gosherve": {
                    "override": "replace",
                    "summary": "gosherve",
                    "command": "/gosherve",
                    "startup": "enabled",
                    "environment": gosherve_env,
                }
            },
        }

        container = self.unit.get_container("gosherve")

        if not container.can_connect():
            self.unit.status = WaitingStatus("waiting for Pebble in workload container")
        else:
            services = container.get_plan().to_dict().get("services", {})
            if services != gosherve_layer["services"]:
                container.add_layer("gosherve", gosherve_layer, combine=True)
                container.restart("gosherve")

        self.unit.status = ActiveStatus()

    def _reconcile_ingress(self, _event=None) -> None:
        if self.desired.ingress == self.actual.ingress:
            return

        self.unit.status = MaintenanceStatus("Updating ingress")
        self.ingress = set_ingress(self, self.ingress, self.desired.ingress)

    def _reconcile_site_content(self, _event=None) -> None:
        if self.desired.site_content == self.actual.site_content:
            return

        self.unit.status = MaintenanceStatus("Fetching web site")
        set_site_content(self.desired.site_content)

        self.unit.status = ActiveStatus()

    def _pull_site_action(self, event) -> None:
        self._reconcile_site_content()
        event.set_results({"result": "site pulled"})


if __name__ == "__main__":
    main(HelloKubeconCharm)
