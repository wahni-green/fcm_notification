# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


import frappe
from frappe.desk.form.assign_to import add, remove

def todo_on_update(doc, method):
	if getattr(frappe.local, "todo_assignment_in_progress", False):
		return

	if not doc.has_value_changed("allocated_to"):
		return

	try:
		frappe.local.todo_assignment_in_progress = True
		current_assigned = frappe.parse_json(doc.get("_assign") or "[]")
		for user in current_assigned:
			remove(doc.doctype, doc.name, user, ignore_permissions=True)

		if doc.allocated_to:
			add({
				"doctype": doc.doctype,
				"name": doc.name,
				"assign_to": [doc.allocated_to]
			}, ignore_permissions=True)

	finally:
		frappe.local.todo_assignment_in_progress = False