// Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
// For license information, please see license.txt


frappe.ui.form.on("Notification Broadcast", {
	refresh(frm) {
        if (
            frm.doc.docstatus == 1
            && frm.doc.is_reusable 
            && frm.doc.cool_down_time < frappe.datetime.now_datetime()
        ) {
            frm.add_custom_button(__("Re-Send"), () => {
                frappe.dom.freeze("Sending Notifications...")
                frappe.call({
                    method: "send_bulk_notifications",
                    doc: frm.doc,
                    callback: (r) => {
                        frappe.dom.unfreeze()
                        frm.refresh();
                    }
                })
            })
        }
	},
});