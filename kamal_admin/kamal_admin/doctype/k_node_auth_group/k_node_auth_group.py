# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class KNodeAuthGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from kamal_admin.kamal_admin.doctype.k_role_assignment.k_role_assignment import KRoleAssignment

		default_for_node_pool_roles: DF.TableMultiSelect[KRoleAssignment]
		description: DF.SmallText | None
		title: DF.Data | None
	# end: auto-generated types

	def as_deploy_dict(self) -> dict:
		return 'self.title'
