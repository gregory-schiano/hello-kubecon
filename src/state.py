from ops.charm import CharmBase

from .gosherve import calculate_env as calculate_gosherve_env
from .gosherve import get_redirect_map as get_gosherve_redirect_map
from .ingress import get as get_ingress
from .ingress import set_ as set_ingress
from .site_ import get_local_content as get_actual_site_content
from .site_ import get_remote_content as get_desired_site_content
from .site_ import set_local_content as set_actual_site_content
from .types_ import Ingress


class Desired:
    def __init__(self, charm: CharmBase) -> None:
        self._charm = charm

    @property
    def ingress(self) -> Ingress:
        return {
            "external-hostname": self.charm.config["external-hostname"]
            or self.charm.app.name,
            "service-name": self.charm.app.name,
            "service-port": 8080,
        }

    @property
    def redirect_map(self) -> str:
        return self.charm.config["redirect-map"]

    @property
    def site_content(_self) -> str:
        return get_desired_site_content()


class ContainerConnectionError(Exception):
    """Errors with connectivity to the container."""


class Actual:
    def __init__(self, charm: CharmBase) -> None:
        self._charm = charm

    @property
    def ingress(self) -> Ingress | None:
        return get_ingress(self.charm.ingress)

    @ingress.setter
    def ingress(self, value: Ingress) -> None:
        self.charm.ingress = set_ingress(self.charm, self.charm.ingress)

    @property
    def redirect_map(self) -> str | None:
        container = self.charm.unit.get_container("gosherve")

        if not container.can_connect():
            return None

        services_info = container.get_plan().to_dict().get("services", {})

        if "gosherve" not in services_info["services"]:
            return None

        gosherve_service = services_info["services"]["gosherve"]

        return get_gosherve_redirect_map(gosherve_service["environment"])

    @redirect_map.setter
    def redirect_map(self, value: str) -> None:
        gosherve_env = calculate_gosherve_env(value)
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

        if container.can_connect():
            raise ContainerConnectionError()

        services = container.get_plan().to_dict().get("services", {})
        if services != gosherve_layer["services"]:
            container.add_layer("gosherve", gosherve_layer, combine=True)
            container.restart("gosherve")

    @property
    def site_content(_self) -> str:
        return get_actual_site_content()

    @site_content.setter
    def site_content(_self, value: str) -> None:
        set_actual_site_content(value)
