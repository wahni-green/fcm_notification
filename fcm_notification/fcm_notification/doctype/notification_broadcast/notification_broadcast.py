# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import scrub
from frappe.utils import now, add_to_date
from frappe.model.document import Document
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
from frappe.utils.user import get_users_with_role

from fcm_notification.firebase import send_notification


class NotificationBroadcast(Document):
	def on_submit(self):
		self.send_bulk_notifications()

	@frappe.whitelist()
	def send_bulk_notifications(self):
		if self.is_reusable:
			minutes = frappe.get_single_value(
				"FCM Settings", "cool_down_time"
			)
			self.db_set("cool_down_time",
				add_to_date(now(), minutes=minutes)
			)

		send_notification({
			"title": self.notification_title,
			"body": self.notification_context,
			"token": frappe.db.get_value("User", frappe.session.user, "fcm_token"),
			"method": "TOKEN",
		})

		user_list = []
		role_doc = frappe.get_doc("Role", self.user_type_to_send_notification)
		if role_doc.is_fcm_role:
			user_list = get_users_with_role(self.user_type_to_send_notification)

		notification_doc = {
			"subject": self.notification_title,
			"email_content": self.notification_context,
			"type": "Alert",
			"from_user": frappe.session.user,
			"from_fcm": 1
		}

		enqueue_create_notification(user_list, notification_doc)

		return True


def create_notification_log(user_list, notification_doc):
	if not frappe.get_single_value("FCM Settings", "enabled"):
		return

	for user in user_list:
		doc = frappe.get_doc({
			"doctype": "Notification Log",
			"subject": notification_doc.get("subject"),
			"email_content": notification_doc.get("email_content"),
			"type": notification_doc.get("type") or "Alert",
			"for_user": user,
			"from_user": notification_doc.get("from_user"),
			"from_fcm": notification_doc.get("from_fcm") or 0
		})
		doc.insert(ignore_permissions=True)