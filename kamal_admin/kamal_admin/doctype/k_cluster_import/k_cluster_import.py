# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

import yaml

import frappe
from frappe.model.document import Document


class KClusterImport(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		import_yaml: DF.LongText | None
		last_import: DF.Datetime | None
		latest_status: DF.Data | None
	# end: auto-generated types

	@frappe.whitelist()
	def import_btn(self):
		log_doc = frappe.get_doc({
			"doctype": "K Cluster Import Log",
			'import_yaml': self.import_yaml,
		})

		cluster_dict = None

		try:
			cluster_dict = yaml.safe_load(self.import_yaml)
		except yaml.YAMLError as e:
			# log_doc.status = "Fail"
			log_doc.error_log = f"YAML parsing error: {str(e)}"
		except Exception as e:
			frappe.log_error(f"Error importing cluster")
			# log_doc.status = "Fail"
			log_doc.error_log = f"Unexpected error: {str(e)}"

		if cluster_dict:
			from kamal_admin.kamal_admin.doctype.k_cluster.k_cluster import KCluster

			try:
				if cluster_doc := KCluster.import_from_dict(log_doc, cluster_dict):
					log_doc.cluster = cluster_doc.name
					# log_doc.status = "Success"

			except Exception as e:
				frappe.log_error(f"Error importing cluster")
				log_doc.error_log = f"Cluster import error: {str(e)}"

		log_doc.insert()
		self.latest_status = log_doc.status
		self.last_import = log_doc.creation

		self.save()


