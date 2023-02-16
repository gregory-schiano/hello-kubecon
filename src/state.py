from typing import Optional

from ops.charm import CharmBase

from gosherve import get_redirect_map as get_gosherve_redirect_map
from ingress import get as get_ingress
from site_ import get_local_content as get_local_site_content
from site_ import get_remote_content as get_remote_site_content
from types_ import Ingress


class Requested:
    def __init__(self, charm: CharmBase) -> None:
        self._charm = charm

    @property
    def ingress(self) -> Ingress:
        return {
            "external-hostname": self._charm.config["external-hostname"]
            or self._charm.app.name,
            "service-name": self._charm.app.name,
            "service-port": 8080,
        }

    @property
    def redirect_map(self) -> str:
        return self._charm.config["redirect-map"]

    @property
    def site_content(_self) -> str:
        return get_remote_site_content()


class Current:
    def __init__(self, charm: CharmBase) -> None:
        self._charm = charm

    @property
    def ingress(self) -> Optional[Ingress]:
        return get_ingress(self._charm.ingress)

    @property
    def redirect_map(self) -> Optional[str]:
        container = self._charm.unit.get_container("gosherve")

        if not container.can_connect():
            return None

        services_info = container.get_plan().to_dict().get("services", {})

        if (
            "services" not in services_info
            or "gosherve" not in services_info["services"]
        ):
            return None

        gosherve_service = services_info["services"]["gosherve"]

        return get_gosherve_redirect_map(gosherve_service["environment"])

    @property
    def site_content(_self) -> Optional[str]:
        return get_local_site_content()
