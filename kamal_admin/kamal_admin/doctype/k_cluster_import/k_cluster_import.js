// Copyright (c) 2025, IQ GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("K Cluster Import", {
	// refresh(frm) {
	// },
	import_btn(frm) {
		frm.call("import_btn");
	},

	display_import_history_btn(frm) {
		frappe.set_route("List", "K Cluster Import Log", "List")
	}
});

