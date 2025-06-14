from setuptools import setup, find_packages

setup(
    name="kamal_admin_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'typer>=0.9',
        'ansible>=9.0',
        'etcd3',
        'hcloud',
        'pyyaml',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'kdep=cli.main:app',
        ],
    },
)
