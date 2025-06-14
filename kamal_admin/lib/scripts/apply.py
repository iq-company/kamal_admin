from scripts.reconcile import reconcile
from scripts.hetzner_provision import provision


def apply(dry: bool = False):
    # reconciliert + provisioniert in einem Rutsch
    provision(dry)
    reconcile(dry)
