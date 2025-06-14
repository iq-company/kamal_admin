# Kamal Infrastructure Admin
Dieses Projekt stellt eine CLI bereit, um komplexe Server-Cluster via Ansible zu verwalten.
CLI Command: kdep (Kamal DEPloy)

## Features
- Multi-Provider-Support (VPS manuell oder Cloud APIs)
- Bastion-Host / ProxyJump für interne Nodes
- NAT-Gateway-Definition
- Label- und Tag-basierte Selektion
- Dezentrales SSH-Key-Management via etcd
- Playbooks für UFW, Fail2Ban, Docker, Prometheus
- Automatische Node-Registrierung und Metriken-Sammlung

## Installation
```bash
# Clone Repo
git clone https://github.com/dein-org/cluster-orchestrator.git
cd cluster-orchestrator
# Python-Abhängigkeiten installieren
pip install -r requirements.txt
```

## CLI Usage
```bash
## Quick‑Start
```bash
# Install prerequisites
pip install -r requirements.txt
ansible-galaxy collection install hetzner.hcloud

# Build & install CLI
pip install .

# Provision zwei Worker + einen Manager in Hetzner‑Cloud
export HCLOUD_TOKEN="<your‑token>"

# neues Cluster‑File generieren (Web‑UI) und anwenden
kdep -c europe-prod.yml reconcile     # Ist ↔ Soll ausgleichen
kdep scale web 8                      # z.B. Autoscaling‑Hook

```
### Keyed Groups
`keyed_groups` in `hcloud.yml` erzeugt dynamische Gruppen aus Labels:
* VM‐Label `role=worker` ⇒ Gruppe `role_worker`
* VM‐Label `env=prod`   ⇒ Gruppe `env_prod`

So kannst du Playbooks oder `kdep`‐Filter auf Gruppen anwenden (`--limit role_worker`).

### cluster.yml = cluster definition
Apply configuration to cluster: `kdep -c cluster.yml apply` (opt. `--dry`)
Dry run: `kdep -c cluster.yml --dry apply`

### Netzwerke definieren
* `type: public`  → reserviertes Label, kein API‑Aufruf
* `type: private` + `create: true` → wird über Hetzner‑API angelegt, inkl. erstem Subnetz
* `ipv4_range` & `subnet_size` – Range & Subnetz‑CIDR für automatische Subnetze

### Public‑IP‑Flags
* `public_ipv4`, `public_ipv6` – granular steuerbar

# explizite Config‑Datei übergeben

### NAT & Firewall
* Setze `nat: true` im Host‑Template → Rolle `nat` + Masquerading aktiviert.
* Andere Hosts können `nat_gw: <name_prefix>` referenzieren; aktuell rein informativ, zukünftige Routen möglich.
* Definiere `open_tcp`, `open_udp` Arrays, damit nftables Port‑Öffnungen generiert werden – vor Docker‑Chains.

