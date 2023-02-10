from charms.nginx_ingress_integrator.v0.ingress import IngressRequires
from ops.charm import CharmBase

from .types_ import Ingress


def get(ingress_requires: None | IngressRequires) -> None | Ingress:
    if ingress_requires is None:
        return None

    return {
        key: value
        for key, value in ingress_requires.config_dict
        if key in Ingress.__required_keys__
    }


def set_(
    charm: CharmBase, ingress_requires: None | IngressRequires, ingress_config: Ingress
) -> IngressRequires:
    if ingress_requires is None:
        return IngressRequires(charm, ingress_config)

    ingress_requires.update_config(ingress_config)
    return ingress_requires
