import logging
from typing import Optional

from charms.nginx_ingress_integrator.v0.ingress import IngressRequires
from ops.charm import CharmBase

from types_ import Ingress


def get(ingress_requires: Optional[IngressRequires]) -> Optional[Ingress]:
    if ingress_requires is None or ingress_requires.config_dict is None:
        return None

    ingress_requires_config = {
        key: value
        for key, value in ingress_requires.config_dict.items()
        if key in {"service-hostname", "service-name", "service-port"}
    }
    ingress_config = {**ingress_requires_config}
    ingress_config["external-hostname"] = ingress_config.pop("service-hostname")
    return ingress_config


def set_(
    charm: CharmBase,
    ingress_requires: Optional[IngressRequires],
    ingress_config: Ingress,
) -> IngressRequires:
    ingress_requires_config = {**ingress_config}
    ingress_requires_config["service-hostname"] = ingress_requires_config.pop(
        "external-hostname"
    )

    if ingress_requires is None:
        return IngressRequires(charm, ingress_requires_config)

    ingress_requires.update_config(ingress_requires_config)
    return ingress_requires
