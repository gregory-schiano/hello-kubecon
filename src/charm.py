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

from state import Actual, ContainerConnectionError, Desired


class HelloKubeconCharm(CharmBase):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.framework.observe(self.on.install, self._reconcile)
        self.framework.observe(self.on.config_changed, self._reconcile)
        self.framework.observe(self.on.gosherve_pebble_ready, self._reconcile)

        self.framework.observe(self.on.pull_site_action, self._pull_site_action)

        self.ingress = None
        self.actual = Actual(self)
        self.desired = Desired(self)

        self._reconcile()

    def _reconcile(self, _event=None) -> None:
        try:
            if self.desired.ingress != self.actual.ingress:
                self.unit.status = MaintenanceStatus("Updating ingress")
                self.actual.ingress = self.desired.ingress

            if self.desired.redirect_map != self.actual.redirect_map:
                self.unit.status = MaintenanceStatus("Setting redirect map")
                self.actual.redirect_map = self.desired.redirect_map

            if self.desired.site_content != self.actual.site_content:
                self.unit.status = MaintenanceStatus("Fetching web site")
                self.actual.site_content = self.desired.site_content

            self.unit.status = ActiveStatus()

        except ContainerConnectionError:
            self.unit.status = WaitingStatus("waiting for Pebble in workload container")

    def _pull_site_action(self, event) -> None:
        self._reconcile()
        event.set_result({"result": "site pulled"})


if __name__ == "__main__":
    main(HelloKubeconCharm)
