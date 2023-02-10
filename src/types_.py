from typing import Protocol, TypedDict

Ingress = TypedDict(
    "Ingress", {"external-hostname": str, "service-name": str, "service-port": int}
)


class CharmState(Protocol):
    ingress: Ingress
    redirect_map: str
    site_content: str
