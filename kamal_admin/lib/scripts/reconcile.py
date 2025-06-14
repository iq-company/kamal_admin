from __future__ import annotations

import os
import typer
from typing import Dict, List
from hcloud import Client
from scripts.cluster_config import load as load_cfg
from rich.console import Console

console = Console()
app = typer.Typer(help="Synchronisiere Cloud-Ist mit cluster.yml-Soll")
client = Client(token=os.getenv("HCLOUD_TOKEN"))


def _current_and_mapping():
    """
    Liest alle Server, baut:
     - name_map: Name → Server
     - role_map: Rolle → [Server, …]
    anhand von Labels role_<rolename>: "true"
    """
    servers = client.servers.get_all()
    name_map: Dict[str, object] = {s.name: s for s in servers}
    role_map: Dict[str, List[object]] = {}
    for s in servers:
        for label, val in s.labels.items():
            if not label.startswith("role_") or str(val).lower() != "true":
                continue
            role = label[len("role_"):]
            role_map.setdefault(role, []).append(s)
    return name_map, role_map


def _build_labels(cluster: str, tmpl: dict) -> Dict[str, str]:
    """
    Erzeugt pro Host-Template das Label-Dictionary
    (ein Label pro Rolle/Auth-Group plus offene Ports & Reporting)
    """
    labels: Dict[str, str] = {"cluster": cluster}
    # ein Label role_<r> = "true" pro Rolle
    for r in tmpl.get("roles", []):
        labels[f"role_{r}"] = "true"
    # ein Label auth_<g> = "true" pro Auth-Group
    for g in tmpl.get("auth_groups", []):
        labels[f"auth_{g}"] = "true"
    return labels


@app.command()
def reconcile(dry: bool = typer.Option(False, "--dry", help="Nur anzeigen")):
    """
    1) Liest cluster.yml
    2) Löscht überschüssige VMs je Host-Template
    3) Aktualisiert Labels auf den verbleibenden VMs
    """
    cfg = load_cfg()
    cluster = cfg["cluster_name"]
    name_map, _role_map = _current_and_mapping()

    for tmpl in cfg.get("hosts", []):
        prefix = f"{cluster}-{tmpl['name_prefix']}"
        # existierende VMs nach Präfix
        existing = [s for n, s in name_map.items() if n.startswith(prefix)]
        desired = tmpl.get("count", 0)
        current = len(existing)
        console.print(f"Template '{tmpl['name_prefix']}': soll {
                      desired}, ist {current}")

        console.print(f"Template '{tmpl['name_prefix']}': soll {
                      desired}, ist {current}")

        # 1) delete overflow
        if current > desired:
            overflow = existing[desired:]
            console.print(f"  → lösche {len(overflow)} überzählige VMs")
            if not dry:
                for s in overflow:
                    s.delete()

        # 2) update labels
        labels = _build_labels(cluster, tmpl)
        for s in existing[:desired]:
            # prüfen, ob sich etwas ändert
            changed = any(labels[k] != s.labels.get(k, None) for k in labels)
            if changed:
                console.print(f"  ↻ aktualisiere Labels auf {s.name}")
                if not dry:
                    s.update(labels=labels)


if __name__ == "__main__":
    app()
