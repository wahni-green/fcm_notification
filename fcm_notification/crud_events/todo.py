# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


import frappe

def todo_after_insert(doc, method):
	if doc.allocated_to:
		frappe.db.set_value("ToDo", doc.name, {
			"_assign": frappe.as_json([doc.allocated_to]),
			"reference_type": "ToDo",
			"reference_name": doc.name
		})

def todo_on_update(doc, method):
	if doc.allocated_to:
		frappe.db.set_value("ToDo", doc.name, {
			"_assign": frappe.as_json([doc.allocated_to]),
			"reference_type": "ToDo",
			"reference_name": doc.name
		})
	else:
		frappe.db.set_value("ToDo", doc.name, {
			"_assign": None,
			"reference_type": None,
			"reference_name": None
		})