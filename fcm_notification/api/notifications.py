# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


import frappe
from fcm_notification.api.utils import log_and_structure
from frappe.utils import strip_html


@frappe.whitelist(methods=["GET"])
@log_and_structure
def fetch_notifications():
	notification_list = frappe.db.get_all("Notification Log",
		{"for_user": frappe.session.user},
		["*"]
	)

	for notification in notification_list:
		notification["subject"] = strip_html(notification["subject"])
		notification["email_content"] = strip_html(notification["email_content"])

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

	user = frappe.session.user
	
	if not fcm_token:
		return {
			"success": False,
			"message": "FCM token is required",
		}
		
	user_doc = frappe.get_doc("User", user)
	user_doc.fcm_token = fcm_token
	user_doc.save(ignore_permissions=True)

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
