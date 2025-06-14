import subprocess
import typer
import sys

app = typer.Typer(help="CLI für Cluster Orchestration")

INVENTORY = "../ansible/inventory.yml"
PLAYBOOK_DIR = "../ansible"


def run_ansible(playbook: str, extra_args: list[str] = []):
    cmd = ["ansible-playbook", "-i", INVENTORY, f"{PLAYBOOK_DIR}/{playbook}"] + extra_args
    result = subprocess.run(cmd)
    if result.returncode != 0:
        typer.echo("Fehler beim Ausführen von Ansible", err=True)
        sys.exit(result.returncode)

@app.command()
def status():
    """Zeigt den Status aller Nodes an"""
    run_ansible("site.yml", ["--tags", "status"])

@app.command()
def update():
    """Führt Updates auf allen Nodes durch"""
    run_ansible("site.yml", ["--tags", "update"])

@app.command()
def deploy(service: str, nodes: str = typer.Option(..., help="Label oder Gruppe der Nodes")):
    """Deployt einen Container-Service"""
    run_ansible("site.yml", ["--tags", "deploy", "-e", f"service={service}", "-e", f"nodes={nodes}"])

@app.command()
def ssh(node: str):
    """SSH-Verbindung zu einem Node aufbauen"""
    typer.echo(f"Verbinde zu {node}...")
    run_ansible("site.yml", ["--tags", "ssh", "-e", f"target={node}"])

if __name__ == "__main__":
    app()

