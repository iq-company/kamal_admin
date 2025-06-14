### Kamal Admin

Adds UI, monitoring, deploy and control interface for kamal deploy

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app kamal_admin
```

### TODO
- [ ] Create DevContainers Setup
- [ ] Display Pools within Cluster in a Virtual Doctype (in Overview Tab)
- [ ] Display Nodes within Cluster in a Virtual Doctype (in Overview Tab)
- [ ] Display Scheduled Changes / States of Assets (Nodes are assets too) within Cluster in a Virtual Doctype (in Overview Tab)
- [ ] Import Filter: error from import to Import Logs Link
- [ ] Import: Import Cluster Node Pools
- [ ] Import: Import Cluster Nodes
- [ ] Add Ansible Scripts for Node Worker Roles
- [ ] Run: Make it runnable / Working
- [ ] Run: Import running infrastructure to empty tenant with yml
- [ ] Run: Generate Diffs before run
- [ ] Generate Kamal Deployment Stacks
- [ ] Run Kamal Deployment Stacks: Get it working

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/kamal_admin
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
