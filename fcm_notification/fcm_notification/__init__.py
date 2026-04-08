# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType

def get_users_with_role(role: str) -> list[str]:
	User = DocType("User")
	HasRole = DocType("Has Role")

	return (
		frappe.qb.from_(HasRole)
		.from_(User)
		.where(
			(HasRole.role == role)
			& (User.name != "Administrator")
			& (User.fcm_token.isnotnull())
			& (User.enabled == 1)
			& (HasRole.parent == User.name)
		)
		.select(User.name)
		.distinct()
		.run(pluck=True)
	)