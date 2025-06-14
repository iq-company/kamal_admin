// Copyright (c) 2024, IQ GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("K Infrastructure Provider", {
	refresh(frm) {
		frm.events.refresh_vm_types_in_node_defs(frm);
	},

	refresh_vm_types_in_node_defs(frm) {
		const fields = frm.doc.assets.filter(a => a.asset_type === "VPS" && a.asset_id).map(a => a.asset_id);

		frm.fields_dict.node_definitions.grid.update_docfield_property(
			"vm_type",
			"options",
			[""].concat(fields)
		);
	}
});

// change VM-Type from Assets to node_definitions vm_type
frappe.ui.form.on("K Infrastructure Provider Asset", {
	asset_type(frm, cdt, cdn) {
		frm.events.refresh_vm_types_in_node_defs(frm);
	},
	asset_id(frm, cdt, cdn) {
		frm.events.refresh_vm_types_in_node_defs(frm);
	}
});

frappe.ui.form.on("K Infrastructure Provider Node Def", {
	vm_type(frm, cdt, cdn) {
		frm.script_manager.trigger("initTitle", cdt, cdn);
	},
	image(frm, cdt, cdn) {
		frm.script_manager.trigger("initTitle", cdt, cdn);
	},

	initTitle(frm, cdt, cdn) {
		const row = frappe.get_doc(cdt, cdn);
		const newTitle = `${row.vm_type || ''} | ${row.image || ''}`;

		if (!row.title || newTitle.startsWith(row.title)) {
			row.title = newTitle;

			frm.refresh_field("node_definitions");
		}
	}
});

