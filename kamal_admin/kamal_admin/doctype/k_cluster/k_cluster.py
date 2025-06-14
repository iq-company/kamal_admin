# Copyright (c) 2024, IQ GmbH and contributors
# For license information, please see license.txt

import yaml

import frappe
from frappe.model.document import Document


class KCluster(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from kamal_admin.kamal_admin.doctype.k_cluster_network.k_cluster_network import KClusterNetwork
		from kamal_admin.kamal_admin.doctype.k_cluster_secret.k_cluster_secret import KClusterSecret

		generated_code: DF.Code | None
		git_repository: DF.Data | None
		network_zones: DF.Table[KClusterNetwork]
		path_prefix: DF.Data | None
		secrets: DF.Table[KClusterSecret]
		service_prefix: DF.Data | None
	# end: auto-generated types

	def before_validate(self):
		# check at least one public network is there and has a title
		public_network = next((n for n in self.network_zones if n.public), None)
		if not public_network:
			public_network = self.append('network_zones', {'public': True})

		if not public_network.title:
			public_network.title = 'Public'

		if public_network.infrastructure_provider:
			public_network.infrastructure_provider = None

	def validate(self):
		# max one network may have public indicator set
		if len([1 for n in self.network_zones if n.public]) > 1:
			frappe.throw("Only one network zone may be public")

		# validate the network names are unique within this cluster
		if len(set([n.title for n in self.network_zones])) != len(self.network_zones):
			frappe.throw("Network zone titles must be unique within a cluster")

		# validate the secret names are unique within this cluster
		if len(set([n.secret_name for n in self.secrets])) != len(self.secrets):
			frappe.throw("Secret Names must be unique within a cluster")

	@property
	def generated_code(self):
		return getattr(self, '_generated_code', None)

	@frappe.whitelist()
	def generate_cluster_yml(self):
		self._generated_code = yaml.dump(convert_dict_bools(self.generate_cluster_deploy_dict()), sort_keys=False, default_flow_style=False)


	def generate_cluster_deploy_dict(self) -> dict:
		if self.is_new():
			return {}

		res = {
			"cluster_name": self.name,
			"service_prefix": self.service_prefix or "",
			"git_repository": self.git_repository or "",
			"path_prefix": self.path_prefix or "",

			"networks": {
				zone.title: {
					"type": "public",
					**({
							"type": "private",
							"ipv4_range": zone.ipv4_range,
							"subnet_size": zone.subnet_size,
							**({
								"network_zone": frappe.db.get_value("K Infrastructure Provider Network Zone", zone.network_zone, "zone"),
								"infrastructure_provider": zone.infrastructure_provider,
							} if zone.network_zone and zone.infrastructure_provider else {}),
						} if not zone.public else {})
				} for zone in self.network_zones
			},

			"node_pools": [
				frappe.get_doc("K Cluster Node Pool", h['name']).as_deploy_dict() for h in frappe.get_all("K Cluster Node Pool", filters={'cluster': self.name})
			],

			"hosts": [
				# TODO
			],

			"secrets": {
				secret.secret_name: {
					"secret_type": secret.secret_type,
				} for secret in self.secrets if secret.secret_name
			}
		}

		return res

	def update_from_dict(self, log_doc, data: dict):
		"""
		Update a cluster from a dictionary.
		"""
		self.update({
			"service_prefix": data.get("service_prefix", self.service_prefix),
			"git_repository": data.get("git_repository", self.git_repository),
			"pth_prefix": data.get("path_prefix", self.path_prefix),
		})

		if networks := data.get("networks"):
			for network_title, network_settings in networks.items():
				# check if network with title is already present
				if not (network_zone_doc := next((n for n in self.network_zones if n.title == network_title), None)):
					network_zone_doc = self.append('network_zones', {'title': network_title})

				network_zone_title = network_settings.pop("network_zone", None)
				network_zone_doc.update(network_settings)

				# check if given infrastructure provider is known
				if network_zone_doc.infrastructure_provider:
					if not frappe.db.exists("K Infrastructure Provider", network_zone_doc.infrastructure_provider):
						frappe.throw(f"Infrastructure provider {network_zone_doc.infrastructure_provider} does not exist")

					infrastructure_provider = frappe.get_doc("K Infrastructure Provider", network_zone_doc.infrastructure_provider)

					if not (network_zone_id := next((nz for nz in infrastructure_provider.network_zones if nz.zone == network_zone_title), None)):
						frappe.throw(f"Network zone {network_zone_title} does not exist in infrastructure provider {network_zone_doc.infrastructure_provider}")

					network_zone_doc.network_zone = network_zone_id.name

		if secrets := data.get("secrets"):
			for secret_name, secret_settings in secrets.items():
				# check if secret with name is already present
				if not (secret_doc := next((s for s in self.secrets if s.secret_name == secret_name), None)):
					secret_doc = self.append('secrets', {'secret_name': secret_name})
					log_doc.warn(f"Secret '{secret_name}' was generated during import: Value needs to be provided!!")

				secret_doc.update(secret_settings)

	@classmethod
	def import_from_dict(cls, log_doc, data: dict):
		"""
		Import (could also update) a cluster from a dictionary.
		"""
		if not data.get("cluster_name"):
			frappe.throw("Cluster name is required for import")

		# check if cluster exists
		if frappe.db.exists("K Cluster", data["cluster_name"]):
			cluster_doc = frappe.get_doc("K Cluster", data["cluster_name"])
		else:
			cluster_doc = frappe.get_doc({
				"doctype": "K Cluster",
			})

			cluster_doc.insert(set_name=data["cluster_name"])

		cluster_doc.update_from_dict(log_doc, data)
		cluster_doc.save()

		# TODO: Import Node Pools
		# TODO: Import Nodes

		return cluster_doc

def convert_dict_bools(d):
	if isinstance(d, dict):
		return {k: convert_dict_bools(v) for k, v in d.items()}
	elif isinstance(d, list):
		return [convert_dict_bools(i) for i in d]
	elif d == 1:
		return True
	elif d == 0:
		return False
	else:
		return d

