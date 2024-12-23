// Copyright (c) 2024, IQ GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on("K Cluster", {
	refresh(frm) {

		this.resetNodes(frm);
	},

	resetNodes(frm) {
		// const nodesParent = frm.page.parent.querySelector(".frappe-control[data-fieldtype=HTML][data-fieldname=nodes_area]");

		// frappe.router.make_url("desk#List/K Node")
		// 	.then((url) => {
		// 	nodesParent.innerHTML = `<iframe src='${url}' style='width: 100%; height: 100%; border: none;'></iframe>`;
		// 	});
		// nodesParent.innerHTML = "<iframe src='/desk#List/K Node' style='width: 100%; height: 100%; border: none;'></iframe>";
	}
});

