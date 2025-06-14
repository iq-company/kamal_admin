// Copyright (c) 2024, IQ GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("K Cluster", {
	refresh(frm) {
		// this.resetNodes(frm);
		frm.set_query("network_zone", "network_zones", function (doc, cdt, cdn) {
			const network_zone_record = locals[cdt][cdn];

			const filters = [
				["parent", "=", network_zone_record.infrastructure_provider || 'choose_infrastructure_provider'],
			];

			return {
				filters: filters,
			};
		});
	},

	generate_cluster_yml(frm) {
		frm.call("generate_cluster_yml");
	}
});

frappe.ui.form.on("K Cluster Network", {
	infrastructure_provider(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);

		if (!row.infrastructure_provider) {
			// init network_zone if corresponding infrastructure_provider is not set / was cleared
			row.network_zone = null;
		}

		// this.events.adjustTitle(frm, cdt, cdn);
		// frappe.ui.form.handlers[doctype]
		// frm.script_manager.get_handlers("adjustTitle", cdt)
		// .script_manager.trigger(fieldname, doc.doctype, doc.name);
		frm.script_manager.trigger("adjustTitle", cdt, cdn);
	},
	network_zone(frm, cdt, cdn) {
		// this.events.adjustTitle(frm, cdt, cdn);
		frm.script_manager.trigger("adjustTitle", cdt, cdn);
	},
	async adjustTitle(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);

		if (!row.public) {
			let network_zone = row.network_zone;

			if (row.infrastructure_provider && network_zone) {
				// read title of network zone
				const provider = await frappe.db.get_doc("K Infrastructure Provider", row.infrastructure_provider);

				network_zone = provider.network_zones.find(nz => nz.name === network_zone)?.zone;
			}

			row.title = `${row.infrastructure_provider || ''} | ${network_zone || ''}`;

			frm.refresh_field("network_zones");
		}
	}
});

