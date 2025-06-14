from __future__ import annotations

import os
from ipaddress import ip_network
from typing import Dict, Set

import typer
from hcloud import Client
from hcloud.images import Image
from hcloud.networks import Network
from hcloud.networks.client import NetworkSubnet
from hcloud.server_types import ServerType
from hcloud.servers.domain import ServerCreatePublicNetwork

from scripts.cluster_config import load as load_cfg

app = typer.Typer(help="Provisioniert Ressourcen laut cluster.yml")
client = Client(token=os.getenv("HCLOUD_TOKEN"))

# ---------------------------------------------------------------------------
# Netzwerk‑Hilfsfunktionen
# ---------------------------------------------------------------------------


def _nets_by_name() -> Dict[str, Network]:
    return {net.name: net for net in client.networks.get_all()}


def _ensure_networks(cfg: dict, dry: bool) -> Dict[str, Network]:
    default_zone = cfg.get("datacenter")
    nets = _nets_by_name()
    for name, spec in cfg.get("networks", {}).items():
        if spec.get("type") != "private" or name in nets:
            continue
        if not spec.get("create", False):
            typer.echo(f"[!] privates Netz '{
                name}' existiert nicht & create=false")
            continue
        if dry:
            typer.echo(f"[DRY] create network {name} ({spec['ipv4_range']})")
            # Platzhalter-Netz
            nets[name] = Network(id=-1, name=name, client=client)
            continue
        net = client.networks.create(name=name, ip_range=spec["ipv4_range"])
        nets[name] = net
        if sub_size := spec.get("subnet_size"):
            count_sub = spec.get("create_subnets", 1)
            zone = spec.get("network_zone", default_zone)
            for i, ip_net in enumerate(ip_network(spec["ipv4_range"]).subnets(new_prefix=sub_size)):
                if i >= count_sub:
                    break
                subnet = NetworkSubnet(
                    type="cloud", network_zone=zone, ip_range=str(ip_net))
                action = net.add_subnet(subnet)
                action.wait_until_finished()
                # sub_action = client.networks.create_subnet(
                #     network=net,
                #     type="cloud",
                #     network_zone=zone,
                #     ip_range=str(ip_net),
                # )
                # sub_action.wait_until_finished()
    return nets

# ---------------------------------------------------------------------------
# Server‑Provisionierung
# ---------------------------------------------------------------------------


def _existing_names() -> Set[str]:
    return {srv.name for srv in client.servers.get_all()}


@app.command()
def provision(dry: bool = typer.Option(False, "--dry", help="Nur anzeigen, nichts anlegen")):
    """Legt laut cluster.yml fehlende Ressourcen in Hetzner Cloud an."""
    cfg = load_cfg()
    cluster = cfg["cluster_name"]
    default_dc = cfg.get("datacenter")
    image = Image(name=cfg["image"])
    nets = _ensure_networks(cfg, dry)
    existing = _existing_names()
    ssh_keys = client.ssh_keys.get_all()

    for tmpl in cfg.get("hosts", []):
        prefix = f"{cluster}-{tmpl['name_prefix']}"
        srv_type = ServerType(name=tmpl.get("vm_type"))
        dc = tmpl.get("datacenter", default_dc)
        for idx in range(1, tmpl.get("count", 0) + 1):
            name = f"{prefix}-{idx}"
            if name in existing:
                continue

            labels = {
                "cluster": cluster,
                **{f"role_{r}": "true" for r in tmpl.get("roles", [])},
                **{f"auth_{g}": "true" for g in tmpl.get("auth_groups", [])},
            }
            public_net_cfg = ServerCreatePublicNetwork(
                ipv4=None,
                ipv6=None,
                enable_ipv4=tmpl.get("public_ipv4", False),
                enable_ipv6=tmpl.get("public_ipv6", False),
            )
            params = {
                "name": name,
                "server_type": srv_type,
                "image": image,
                "labels": labels,
                "ssh_keys": ssh_keys,
                "public_net": public_net_cfg,
            }
            if dc:
                try:
                    dc_obj = client.datacenters.get_by_name(dc)
                except Exception as e:
                    dc_obj = client.datacenters.get_by_id(dc)

                params["datacenter"] = dc_obj

            privs = [nets[n] for n in tmpl.get(
                "networks", []) if n in nets and nets[n].id != -1]
            if privs:
                params["networks"] = privs

            if dry:
                typer.echo(f"[DRY] create {name:25} → {srv_type.name}")
                continue

            resp = client.servers.create(**params)
            action = resp.action
            server = resp.server
            typer.echo(f"[+] create {name:25} @ {dc} (action {action.id})")
            action.wait_until_finished()


if __name__ == "__main__":
    app()
