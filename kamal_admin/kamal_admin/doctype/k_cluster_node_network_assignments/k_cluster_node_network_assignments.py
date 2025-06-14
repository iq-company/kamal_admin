# Copyright (c) 2025, IQ GmbH and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class KClusterNodeNetworkAssignments(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cluster_network: DF.Link
		hide_ports_behind_ports_opener: DF.Check
		open_ports: DF.Data | None
		openable_ports: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		ports_opener_port: DF.Int
		ports_opener_secret: DF.Link | None
	# end: auto-generated types

	def as_deploy_dict(self) -> dict:
		if self.is_new():
			return {}

		network_doc = frappe.get_doc("K Cluster Network", self.cluster_network)

		res = {
			'network': network_doc.title,
		}

		if (open_ports := parse_ports(self.open_ports)) is not None:
			res['open_ports'] = open_ports

		if self.hide_ports_behind_ports_opener:
			res['ports_opener_secret'] = frappe.db.get_value("K Cluster Secret", self.ports_opener_secret, "secret_name")

			if (ports_opener_port := parse_ports(self.ports_opener_port)):
				res['ports_opener_port'] = ports_opener_port[0] # only one is allowed

			if (openable_ports := parse_ports(self.openable_ports)):
				res['openable_ports'] = openable_ports

		return res

def parse_ports(ports: str | int) -> list[int] | None:
	"""
	Parse a string of ports into a list of integers.
	"""
	if not ports:
		return []

	# if int is given return list of it
	if isinstance(ports, int):
		return [ports]


	if ports.strip() == '*':
		return None

	port_list = []
	for port in ports.split(','):
		port = port.strip()
		if port.isdigit():
			port_list.append(int(port))

	return port_list

