from charms.nginx_ingress_integrator.v0.ingress import IngressRequires
from ops.charm import CharmBase

from types_ import Ingress


def init(
    charm: CharmBase,
    ingress_config: Ingress,
) -> IngressRequires:
    ingress_requires_config = {**ingress_config}
    if "external-hostname" in ingress_requires_config:
        ingress_requires_config["service-hostname"] = ingress_requires_config.pop(
            "external-hostname"
        )

    return IngressRequires(charm, ingress_requires_config)


def update(
    ingress_requires: IngressRequires,
    ingress_config: Ingress,
) -> None:
    ingress_requires_config = {**ingress_config}
    if "external-hostname" in ingress_requires_config:
        ingress_requires_config["service-hostname"] = ingress_requires_config.pop(
            "external-hostname"
        )
    ingress_requires.update_config(ingress_requires_config)
