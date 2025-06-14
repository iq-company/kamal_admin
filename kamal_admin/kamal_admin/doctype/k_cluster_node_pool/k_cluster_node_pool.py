# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class KClusterNodePool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from kamal_admin.kamal_admin.doctype.k_auth_group_assignments.k_auth_group_assignments import KAuthGroupAssignments
		from kamal_admin.kamal_admin.doctype.k_cluster_node_network_assignments.k_cluster_node_network_assignments import KClusterNodeNetworkAssignments
		from kamal_admin.kamal_admin.doctype.k_role_assignment.k_role_assignment import KRoleAssignment

		auth_groups: DF.TableMultiSelect[KAuthGroupAssignments]
		cluster: DF.Link
		cluster_networks: DF.Table[KClusterNodeNetworkAssignments]
		count: DF.Int
		count_max: DF.Int
		infrastructure_provider: DF.Link
		name_prefix: DF.Data | None
		nat_gateway_role: DF.Link | None
		node_definition: DF.Link
		node_roles: DF.TableMultiSelect[KRoleAssignment]
		public_ipv4: DF.Check
		public_ipv6: DF.Check
		report_metrics_to: DF.TableMultiSelect[KRoleAssignment]
		title: DF.Data
	# end: auto-generated types

	def as_deploy_dict(self) -> dict:
		if self.is_new():
			return {}

		# infra_provider_doc = frappe.get_doc("K Infrastructure Provider", self.infrastructure_provider)
		infra_provider_doc = frappe.get_doc("K Infrastructure Provider", self.infrastructure_provider)
		node_definition_doc = next((nd for nd in infra_provider_doc.node_definitions if nd.name == self.node_definition), None)

		res = {
			'name_prefix': self.name_prefix,
			'auth_groups': [g.as_deploy_dict() for g in self.auth_groups],
			'count': self.count,
			# 'count_max': self.count_max,
			'public_ipv4': self.public_ipv4,
			'public_ipv6': self.public_ipv6,
			**({
				'vm_type': node_definition_doc.vm_type,
				'image': node_definition_doc.image
			} if node_definition_doc else {}),
			'roles': [r.as_deploy_dict() for r in self.node_roles],
			'auth_groups': [r.as_deploy_dict() for r in self.auth_groups],
			'networks': [r.as_deploy_dict() for r in self.cluster_networks],
		}

		if self.nat_gateway_role:
			res['nat_gateway_role'] = self.nat_gateway_role

		if self.report_metrics_to:
			res['report_metrics_to'] = [r.as_deploy_dict() for r in self.report_metrics_to]

		return res
