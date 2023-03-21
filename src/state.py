from ops.charm import model

from site_ import get_remote_content as get_remote_site_content
from types_ import Ingress


class State:
    def __init__(self, charm_config: model.ConfigData, charm_name: str) -> None:
        self._charm_config = charm_config
        self._charm_name = charm_name

    @property
    def ingress(self) -> Ingress:
        return {
            "external-hostname": self._charm_config["external-hostname"]
            or self._charm_name,
            "service-name": self._charm_name,
            "service-port": 8080,
        }

    @property
    def redirect_map_url(self) -> str:
        return self._charm_config["redirect-map"]

    @property
    def site_content(_self) -> str:
        return get_remote_site_content()
