from ops.charm import CharmBase

from gosherve import get_redirect_map as get_gosherve_redirect_map
from ingress import get as get_ingress
from site_ import get_local_content as get_local_site_content
from site_ import get_remote_content as get_remote_site_content
from types_ import Ingress


class State:
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
