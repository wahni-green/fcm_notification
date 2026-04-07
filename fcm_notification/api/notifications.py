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

	frappe.db.set_value("Notification Log", notification_list, {"read": 1})

	return{
		"success": True, 
		"message": "Notifications Updated"
	}