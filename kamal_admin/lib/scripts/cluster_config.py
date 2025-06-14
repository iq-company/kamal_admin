import yaml
import pathlib
import tempfile
import shutil
import os
from contextlib import contextmanager

DEFAULT_PATH = pathlib.Path.cwd() / "cluster.yml"


def _path():
    return pathlib.Path(os.getenv("KDEP_CLUSTER_FILE", DEFAULT_PATH))


def load():
    with _path().open() as f:
        return yaml.safe_load(f)


def save(data):
    dest = _path()
    tmp = tempfile.NamedTemporaryFile(delete=False, dir=dest.parent, mode='w')
    yaml.safe_dump(data, tmp)
    tmp.flush()
    tmp.close()
    shutil.move(tmp.name, dest)


@contextmanager
def edit():
    cfg = load()
    yield cfg
    save(cfg)
