// Copyright (c) 2025, IQ GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("K Cluster Node Pool", {
	refresh(frm) {
		// frm.set_query("vm_type", function (doc) {
		// 	const filters = [
		// 		// ["K Infrastructure Provider Asset", "asset_type", "=", "VPS"],
		// 		["parent", "=", frm.doc.infrastructure_provider],
		// 		["asset_type", "=", "VPS"],
		// 	];

		// 	return {
		// 		filters: filters,
		// 	};
		// });
		frm.set_query("ports_opener_secret", "cluster_networks", function (doc, cdt, cdn) {
			const cluster_network_record = frappe.get_doc(cdt, cdn);

			const filters = [
				["parent", "=", frm.doc.cluster || 'choose_cluster'],
				["secret_type", "=", "Password"],
			];

			return {
				filters: filters,
			};
		});

		frm.set_query("report_metrics_to", function (doc) {
			const filters = [
				// ["K Role Assignment", "parent", "=", frm.doc.infrastructure_provider],
				["K Node Role", "native_function", "=", "Monitoring Receiver"],
			];

			return {
				filters: filters,
			};
		});

		frm.set_query("nat_gateway_role", function (doc) {
			const filters = [
				["K Node Role", "native_function", "=", "NAT"],
			];

			return {
				filters: filters,
			};
		});
	},

	async node_roles(frm) {
		const assignedRoleNames = frm.doc.node_roles?.map(r => r.role);
		const concatenatedRoleNames = assignedRoleNames.join(", ");

		if (!frm.doc.title || concatenatedRoleNames.startsWith(frm.doc.title)) {
			frm.set_value("title", concatenatedRoleNames);
		}

		// adjust auth-groups
		if (assignedRoleNames && assignedRoleNames.length > 0) {
			const defaultAuthGroups = await frappe.db.get_list("K Node Auth Group", { filters: [["K Role Assignment", "role", "in", assignedRoleNames]] });

			if (defaultAuthGroups?.length) {
				// check availability of assigned roles
				for (const role of defaultAuthGroups) {
					if (!frm.doc.auth_groups?.find(ag => ag.auth_group === role.name)) {
						// add auth group if not already assigned
						frm.add_child("auth_groups", {
							name: role.name,
							auth_group: role.name,
							role: role.role,
						});
					}
				}

				frm.refresh_field("auth_groups");
			}
		}
	}
});

