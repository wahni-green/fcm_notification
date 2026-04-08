# Copyright (c) 2026, Wahni IT Solutions Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import scrub
from frappe.utils import now, add_to_date
from frappe.model.document import Document
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
from fcm_notification.firebase import send_notification
from fcm_notification import get_users_with_role


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
			"topic": self.fcm_role,
			"method": "TOPIC",
		})

		user_list = get_users_with_role(self.fcm_role)

		notification_doc = {
			"subject": self.notification_title,
			"email_content": self.notification_context,
			"type": "Alert",
			"from_user": frappe.session.user,
			"from_fcm": 1
		}

		enqueue_create_notification(user_list, notification_doc)

		return True