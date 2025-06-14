# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class KRoleAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		role: DF.Link
	# end: auto-generated types

	def as_deploy_dict(self) -> str | None:
		return self.role

