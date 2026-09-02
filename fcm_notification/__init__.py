__version__ = "0.0.1"

import frappe
from frappe.query_builder import DocType

def get_users_with_role(role: str) -> list[str]:
	User = DocType("User")
	HasRole = DocType("Has Role")
	FCMUser = DocType("FCM User")

	return (
		frappe.qb.from_(HasRole)
		.from_(User)
		.from_(FCMUser)
		.where(
			(HasRole.role == role)
			& (User.name != "Administrator")
			& (User.enabled == 1)
			& (HasRole.parent == User.name)
			& (FCMUser.user == User.name)
		)
		.select(User.name)
		.distinct()
		.run(pluck=True)
	)