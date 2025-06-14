# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class KClusterImportLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cluster: DF.Link | None
		error_log: DF.LongText | None
		import_tried_at: DF.Datetime | None
		import_yaml: DF.LongText
		log: DF.LongText | None
		status: DF.Literal["", "Success", "Fail", "Incomplete"]
	# end: auto-generated types

	def before_insert(self):
		# Set the import tried at timestamp.
		if not self.import_tried_at:
			self.import_tried_at = self.creation

		# detect correct status
		if self.cluster:
			if self.error_log:
				self.status = "Fail"
			elif self.log:
				self.status = "Incomplete"
			else:
				self.status = "Success"
		else:
			self.status = "Fail"

	def warn(self, message: str):
		"""Log a warning message."""
		if not self.log:
			self.log = ""

		self.log += "\n[WARN]: " + message

