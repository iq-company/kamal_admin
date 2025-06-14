import typer
import subprocess
import os
from pathlib import Path
from scripts.apply import apply as apply_cluster

app = typer.Typer(help="kdep – bringe den Cluster exakt auf YAML-Sollzustand")
BASE_DIR = Path(__file__).resolve().parent.parent
PLAYBOOK_DIR = BASE_DIR / 'ansible'


@app.callback()
def main(ctx: typer.Context, config: Path = typer.Option(None, '--config', '-c', help='Pfad zur cluster.yml'), dry: bool = typer.Option(False, '--dry', help='Nur anzeigen, nichts ändern')):
    if config:
        os.environ['KDEP_CLUSTER_FILE'] = str(config)
    ctx.obj = {'dry': dry}


@app.command('apply')
def apply_cmd(ctx: typer.Context):
    """Erstellt / entfernt VMs und führt Ansible aus – one‑stop."""
    dry = ctx.obj['dry']
    apply_cluster(dry)
    if not dry:
        _run_ansible()


def _run_ansible():
    subprocess.run(
        ['ansible-playbook', str(PLAYBOOK_DIR / 'site.yml')], check=True)


if __name__ == '__main__':
    app()
