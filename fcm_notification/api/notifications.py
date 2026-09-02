# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


import frappe
from fcm_notification.api.utils import log_and_structure
from frappe.utils import strip_html


@frappe.whitelist(methods=["GET"])
@log_and_structure
def fetch_notifications():
	notification_list = frappe.db.get_all(
		"Notification Log", {"for_user": frappe.session.user}, ["*"]
	)

	for notification in notification_list:
		notification["subject"] = strip_html(notification.get("subject") or "")
		notification["email_content"] = strip_html(notification.get("email_content") or "")

	return{
		"success": True, 
		"message": notification_list or []
	}


@frappe.whitelist(methods=["POST"])
@log_and_structure
def update_notifications(notification_list):
	if isinstance(notification_list, str):
		notification_list = frappe.parse_json(notification_list)

	frappe.db.set_value(
		"Notification Log",
		{
			"name": ["in", notification_list],
			"for_user": frappe.session.user
		},
		"read",
		1
	)

	return{
		"success": True, 
		"message": "Notifications Updated"
	}
 
 
@frappe.whitelist(methods=["POST"])
@log_and_structure
def update_fcm_token(fcm_token=None):
	if not fcm_token:
		return {
			"success": False,
			"message": "FCM token is required",
		}

	user = frappe.session.user

	# Each device registers its own row, keyed by its token — re-registering
	# an existing token (refresh, or the same device logging back in) just
	# repoints it at whoever is signed in now, rather than creating a
	# duplicate row for the same device.
	existing = frappe.db.get_value("FCM User", {"registration_token": fcm_token}, "name")
	if existing:
		frappe.db.set_value("FCM User", existing, "user", user)
	else:
		try:
			frappe.get_doc(
				{
					"doctype": "FCM User",
					"user": user,
					"registration_token": fcm_token,
				}
			).insert(ignore_permissions=True)
		except frappe.DuplicateEntryError:
			# Lost a race with another concurrent registration of this same
			# token (e.g. the app calling initialize() more than once) — the
			# row landed in between our check and insert, just repoint it.
			frappe.db.set_value("FCM User", {"registration_token": fcm_token}, "user", user)

	roles = frappe.get_roles(user)
	fcm_roles = frappe.get_all(
		"Role",
		filters={
			"name": ["in", roles],
			"is_fcm_role": 1
		},
		pluck="name"
	)

	return {
		"success": True,
		"message": "FCM token updated successfully",
		"user": user,
		"fcm_roles": fcm_roles
	}


@frappe.whitelist(methods=["POST"])
@log_and_structure
def remove_fcm_token(fcm_token=None):
	if not fcm_token:
		return {
			"success": False,
			"message": "FCM token is required",
		}

	frappe.db.delete(
		"FCM User",
		{"registration_token": fcm_token, "user": frappe.session.user},
	)

	return {
		"success": True,
		"message": "FCM token removed successfully",
	}
