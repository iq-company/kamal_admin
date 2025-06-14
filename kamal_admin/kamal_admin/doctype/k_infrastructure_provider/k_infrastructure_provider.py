# Copyright (c) 2024, IQ GmbH and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class KInfrastructureProvider(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from kamal_admin.kamal_admin.doctype.k_infrastructure_provider_asset.k_infrastructure_provider_asset import KInfrastructureProviderAsset
		from kamal_admin.kamal_admin.doctype.k_infrastructure_provider_network_zone.k_infrastructure_provider_network_zone import KInfrastructureProviderNetworkZone
		from kamal_admin.kamal_admin.doctype.k_infrastructure_provider_node_def.k_infrastructure_provider_node_def import KInfrastructureProviderNodeDef
		from kamal_admin.kamal_admin.doctype.k_infrastructure_provider_region.k_infrastructure_provider_region import KInfrastructureProviderRegion

		assets: DF.Table[KInfrastructureProviderAsset]
		driver: DF.Literal["Hetzner"]
		network_zones: DF.Table[KInfrastructureProviderNetworkZone]
		node_definitions: DF.Table[KInfrastructureProviderNodeDef]
		regions: DF.Table[KInfrastructureProviderRegion]
	# end: auto-generated types

	pass
