# Copyright (c) 2026, Wahni IT Solutions and contributors
# For license information, please see license.txt


import frappe
from fcm_notifications.api.utils import log_and_structure


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

	return {
		"success": True,
		"message": "FCM token updated successfully",
		"user": user
	}
