# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class KAuthGroupAssignments(Document):
	def as_deploy_dict(self) -> dict:
		return self.auth_group

